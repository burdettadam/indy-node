from indy_common.authorize.auth_actions import AuthActionAdd, AuthActionEdit
from indy_common.authorize.auth_request_validator import WriteRequestValidator

from indy_common.constants import RS_META, RS_DATA, RS_META_VERSION, SET_RS_ENCODING, \
     RS_META_NAME, RS_JSON_LD_ID, RS_META_TYPE

from indy_common.state.state_constants import MARKER_RS_ENCODING
from plenum.common.constants import DOMAIN_LEDGER_ID, DATA

from plenum.common.request import Request
from plenum.common.txn_util import get_from, get_seq_no, get_txn_time, get_payload_data
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.write_request_handler import WriteRequestHandler
from plenum.server.request_handlers.utils import encode_state_value


class RsEncodingHandler(WriteRequestHandler):

    def __init__(self, database_manager: DatabaseManager,
                 write_req_validator: WriteRequestValidator):
        super().__init__(database_manager, SET_RS_ENCODING, DOMAIN_LEDGER_ID)
        self.write_req_validator = write_req_validator

    def _validate(self, meta, encoding):
        pass

    def static_validation(self, request: Request):
        self._validate_request_type(request)  # is this redundant check, how is this code called if txn type is wrong?
        if request.operation[RS_META] is None:
            pass
        if not isinstance(request.operation[RS_META], dict):
            pass
        if request.operation[RS_META][RS_META_TYPE] is None:
            pass
        if not isinstance(request.operation[RS_META][RS_META_TYPE], str):
            pass
        if request.operation[RS_META][RS_META_NAME] is None:
            pass
        if not isinstance(request.operation[RS_META][RS_META_NAME], str):
            pass
        if request.operation[RS_META][RS_META_VERSION] is None:
            pass
        if not isinstance(request.operation[RS_META][RS_META_VERSION], str):
            pass
        if request.operation[RS_DATA] is None:
            pass
        # TODO: validate operation data
        self._validate(request.operation[RS_META], request.operation[RS_DATA])

        author = request.identifier
        name = request.operation[RS_META][RS_META_NAME]
        version = request.operation[RS_META][RS_META_VERSION]
        _id = RsEncodingHandler.make_state_path(author, name, version)

        encoding, _, _ = self.get_from_state(_id)
        if encoding:
            return False  # updating belongs in a different txn.
        else:
            self.write_req_validator.validate(request,
                                              [AuthActionAdd(txn_type=SET_RS_ENCODING,
                                                             field='*',
                                                             value='*')])

    def gen_txn_id(self, txn):
        self._validate_txn_type(txn)
        path = RsEncodingHandler.prepare_state(txn, path_only=True)
        return path.decode()

    def update_state(self, txn, prev_result, request, is_committed=False) -> None:
        self._validate_txn_type(txn)
        path, value_bytes = RsEncodingHandler.prepare_state(txn)
        self.state.set(path, value_bytes)

    @staticmethod
    def prepare_state(txn, path_only=False):
        payload = get_payload_data(txn)
        meta, data = payload[RS_META], payload[DATA]
        did_author = get_from(txn)
        _id = RsEncodingHandler.make_state_path(did_author, meta[RS_META_NAME], meta[RS_META_VERSION])
        if path_only:
            return _id
        data.update({RS_JSON_LD_ID: _id})
        meta.update({RS_META_TYPE: MARKER_RS_ENCODING})
        value = {
            RS_META: meta,
            RS_DATA: data
        }
        seq_no = get_seq_no(txn)
        txn_time = get_txn_time(txn)
        value_bytes = encode_state_value(value, seq_no, txn_time)
        return _id, value_bytes

    @staticmethod
    def make_state_path(authors_did, name, version) -> bytes:
        return "{DID}:{MARKER}:{NAME}:{VERSION}" \
            .format(DID=authors_did,
                    MARKER=MARKER_RS_ENCODING,
                    NAME=name,
                    VERSION=version).encode()
