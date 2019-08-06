from indy_common.authorize.auth_actions import AuthActionAdd, AuthActionEdit
from indy_common.authorize.auth_request_validator import WriteRequestValidator

from indy_common.constants import RS_SCHEMA_LABEL, \
    RS_SCHEMA_CONTEXT, RS_SCHEMA_TYPE, RS_SCHEMA_EXPANDED_DOCUMENT, RS_SCHEMA_VERSION, SET_RS_SCHEMA, RS_SCHEMA_ID

from indy_common.state.state_constants import MARKER_RS_SCHEMA
from plenum.common.constants import DOMAIN_LEDGER_ID, DATA
from plenum.common.exceptions import InvalidClientRequest

from plenum.common.request import Request
from plenum.common.txn_util import get_request_data, get_from, get_seq_no, get_txn_time, get_payload_data
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.write_request_handler import WriteRequestHandler
from plenum.server.request_handlers.utils import encode_state_value
from jsonschema import validate


class RsSchemaHandler(WriteRequestHandler):

    def __init__(self, database_manager: DatabaseManager,
                 write_req_validator: WriteRequestValidator):
        super().__init__(database_manager, SET_RS_SCHEMA, DOMAIN_LEDGER_ID)
        self.write_req_validator = write_req_validator

    def _validate_rs_schema(self, schema_array):
        validate(schema_array)

    def __init__(self, database_manager: DatabaseManager,
                 write_req_validator: WriteRequestValidator):
        super().__init__(database_manager, SET_RS_SCHEMA, DOMAIN_LEDGER_ID)
        self.write_req_validator = write_req_validator

    def static_validation(self, request: Request):
        self._validate_request_type(request)  # is this redundant check?
        assert request.operation[RS_SCHEMA_LABEL] is not None
        assert request.operation[RS_SCHEMA_TYPE] is not None
        assert request.operation[RS_SCHEMA_VERSION] is not None
        assert request.operation[RS_SCHEMA_CONTEXT] is not None
        assert isinstance(request.operation[RS_SCHEMA_CONTEXT], list)
        assert request.operation[RS_SCHEMA_EXPANDED_DOCUMENT] is not None
        assert isinstance(request.operation[RS_SCHEMA_EXPANDED_DOCUMENT], list)
        self._validate_rs_schema(request.operation[RS_SCHEMA_EXPANDED_DOCUMENT])

        dest = request.identifier
        label = request.operation[RS_SCHEMA_LABEL]
        schema_type = request.operation[RS_SCHEMA_TYPE]
        version = request.operation[RS_SCHEMA_VERSION]
        #  context = request.operation[RS_SCHEMA_CONTEXT]
        #  props = request.operation[RS_SCHEMA_EXPANDED_DOCUMENT]
        path = RsSchemaHandler.make_state_path(dest, schema_type, label, version)

        schema, _, _ = self.get_from_state(path)
        if schema:
            self.write_req_validator.validate(request,
                                              [AuthActionEdit(txn_type=RS_SET_SCHEMA,
                                                              field='*',
                                                              old_value='*',
                                                              new_value='*')])
        else:
            self.write_req_validator.validate(request,
                                              [AuthActionAdd(txn_type=RS_SET_SCHEMA,
                                                             field='*',
                                                             value='*')])

    def gen_txn_id(self, txn):
        self._validate_txn_type(txn)
        path = RsSchemaHandler.prepare_state(txn, path_only=True)
        return path.decode()

    def update_state(self, txn, prev_result, request, is_committed=False) -> None:
        self._validate_txn_type(txn)
        path, value_bytes = RsSchemaHandler.prepare_state(txn)
        self.state.set(path, value_bytes)

    @staticmethod
    def prepare_state(txn, path_only=False):
        payload = get_payload_data(txn)[DATA]
        did = get_from(txn)
        schema_type = payload[RS_SCHEMA_TYPE]
        label = payload[RS_SCHEMA_LABEL]
        version = payload[RS_SCHEMA_VERSION]
        path = RsSchemaHandler.make_state_path(did, schema_type, label, version)
        value = {
            RS_SCHEMA_CONTEXT: payload[RS_SCHEMA_CONTEXT],
            RS_SCHEMA_TYPE: schema_type,
            RS_SCHEMA_ID: path,
            RS_SCHEMA_LABEL: label,
            RS_SCHEMA_VERSION: version,
            RS_SCHEMA_EXPANDED_DOCUMENT: payload[RS_SCHEMA_EXPANDED_DOCUMENT]
        }
        if path_only:
            return path
        seq_no = get_seq_no(txn)
        txn_time = get_txn_time(txn)
        value_bytes = encode_state_value(value, seq_no, txn_time)
        return path, value_bytes

    @staticmethod
    def make_state_path(authors_did, schema_type, name, version) -> bytes:
        return "{DID}:{MARKER}:{TYPE}:{NAME}:{VERSION}" \
            .format(DID=authors_did,
                    TYPE=schema_type,
                    MARKER=MARKER_RS_SCHEMA,
                    NAME=name,
                    VERSION=version).encode()
