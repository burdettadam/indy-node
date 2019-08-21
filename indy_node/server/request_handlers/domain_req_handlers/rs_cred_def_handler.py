from indy_common.authorize.auth_actions import AuthActionAdd, AuthActionEdit
from indy_common.authorize.auth_request_validator import WriteRequestValidator

from indy_common.constants import RS_DATA, RS_META, \
    RS_CRED_DEF_SCHEMA_REF, RS_CRED_DEF_MAPPING_REF, SET_RS_SCHEMA, SET_RS_MAPPING, RS_CRED_DEF_SIGNATURE_TYPE, \
    RS_CRED_DEF_CL, RS_CRED_DEF_TAG, RS_CRED_DEF_TAG_DEFAULT, SET_RS_CRED_DEF, RS_CRED_DEF_PUBLIC_KEYS
from indy_common.state.state_constants import MARKER_RS_CRED_DEF

from plenum.common.constants import DOMAIN_LEDGER_ID, TXN_PAYLOAD, TXN_PAYLOAD_METADATA, TXN_PAYLOAD_METADATA_FROM, \
    TXN_METADATA, TXN_METADATA_SEQ_NO, TXN_METADATA_TIME
from plenum.common.exceptions import InvalidClientRequest
from plenum.common.request import Request

from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.write_request_handler import WriteRequestHandler
from plenum.server.request_handlers.utils import encode_state_value


class RsCredDefHandler(WriteRequestHandler):

    def __init__(self, database_manager: DatabaseManager,
                 write_req_validator: WriteRequestValidator):
        super().__init__(database_manager, SET_RS_CRED_DEF, DOMAIN_LEDGER_ID)
        self.write_req_validator = write_req_validator

    def static_validation(self, request: Request):
        pass

    def dynamic_validation(self, request: Request):
        # we can not add a Claim Def with existent ISSUER_DID
        # sine a Claim Def needs to be identified by seqNo
        self._validate_request_type(request)
        identifier, req_id, data, meta = request.identifier, request.reqId, request.operation[RS_DATA],\
                                         request.operation[RS_META]
        schema_ref = data[RS_CRED_DEF_SCHEMA_REF]
        mapping_ref = data[RS_CRED_DEF_MAPPING_REF]
        try:
            schema_txn = self.ledger.get_by_seq_no_uncommitted(schema_ref)
        except KeyError:
            raise InvalidClientRequest(identifier,
                                       req_id,
                                       "Mentioned seqNo ({}) doesn't exist.".format(schema_txn))
        try:
            mapping_txn = self.ledger.get_by_seq_no_uncommitted(mapping_ref)

        except KeyError:
            raise InvalidClientRequest(identifier,
                                       req_id,
                                       "Mentioned seqNo ({}) doesn't exist.".format(mapping_txn))

        if schema_txn['txn']['type'] != SET_RS_SCHEMA:
            raise InvalidClientRequest(identifier,
                                       req_id,
                                       "Mentioned seqNo ({}) isn't seqNo of the schema.".format(schema_txn))
        if mapping_txn['txn']['type'] != SET_RS_MAPPING:
            raise InvalidClientRequest(identifier,
                                       req_id,
                                       "Mentioned seqNo ({}) isn't seqNo of the mapping.".format(mapping_txn))
        signature_type = request.operation[RS_DATA][RS_CRED_DEF_SIGNATURE_TYPE] or RS_CRED_DEF_CL
        tag = request.operation[RS_DATA][RS_CRED_DEF_TAG] or RS_CRED_DEF_TAG_DEFAULT

        path = self.make_state_path(identifier, mapping_txn, signature_type, tag)

        cred_def, _, _ = self.get_from_state(path, is_committed=False)

        if cred_def:
            self.write_req_validator.validate(request,
                                              [AuthActionEdit(txn_type=SET_RS_CRED_DEF,
                                                              field='*',
                                                              old_value='*',
                                                              new_value='*')])
        else:
            self.write_req_validator.validate(request,
                                              [AuthActionAdd(txn_type=SET_RS_CRED_DEF,
                                                             field='*',
                                                             value='*')])

    def gen_txn_id(self, txn):
        self._validate_txn_type(txn)
        path = self.prepare_state(txn, path_only=True)
        return path.decode()

    def update_state(self, txn, prev_result, request, is_committed=False) -> None:
        self._validate_txn_type(txn)
        path, value_bytes = self.prepare_state(txn)
        self.state.set(path, value_bytes)
        return txn

    @staticmethod
    def prepare_state(txn, path_only=False):
        schema_seq_no = txn[TXN_PAYLOAD][RS_DATA][RS_CRED_DEF_SCHEMA_REF]
        if schema_seq_no is None:
            raise ValueError("'{}' field is absent, "
                             "but it must contain schema seq no".format(RS_CRED_DEF_SCHEMA_REF))
        mapping_seq_no = txn[TXN_PAYLOAD][RS_DATA][RS_CRED_DEF_MAPPING_REF]
        if mapping_seq_no is None:
            raise ValueError("'{}' field is absent, "
                             "but it must contain mapping seq no".format(RS_CRED_DEF_MAPPING_REF))
        data = txn[TXN_PAYLOAD][RS_DATA][RS_CRED_DEF_PUBLIC_KEYS]
        if data is None:
            raise ValueError("'{}' field is absent, "
                             "but it must contain components of keys"
                             .format(RS_CRED_DEF_MAPPING_REF))
        signature_type = txn.operation[RS_DATA][RS_CRED_DEF_SIGNATURE_TYPE] or RS_CRED_DEF_CL
        tag = txn.operation[RS_DATA][RS_CRED_DEF_TAG] or RS_CRED_DEF_TAG_DEFAULT
        origin = txn[TXN_PAYLOAD][TXN_PAYLOAD_METADATA][TXN_PAYLOAD_METADATA_FROM] or None
        path = RsCredDefHandler.make_state_path(origin, mapping_seq_no, signature_type, tag)
        if path_only:
            return path
        seq_no = txn[TXN_METADATA][TXN_METADATA_SEQ_NO] or None
        txn_time = txn[TXN_METADATA][TXN_METADATA_TIME] or None
        value_bytes = encode_state_value(data, seq_no, txn_time)
        return path, value_bytes

    @staticmethod
    def make_state_path(authors_did, mapping_seq_no, signature_type, tag) -> bytes:
        return "{DID}:{MARKER}:{SIGNATURE_TYPE}:{SCHEMA_SEQ_NO}:{TAG}" \
            .format(DID=authors_did,
                    MARKER=MARKER_RS_CRED_DEF,
                    SIGNATURE_TYPE=signature_type,
                    SCHEMA_SEQ_NO=mapping_seq_no,
                    TAG=tag).encode()
