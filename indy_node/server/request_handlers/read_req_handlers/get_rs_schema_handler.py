from indy_common.constants import RS_SCHEMA_ID, RS_SCHEMA_LABEL, RS_SCHEMA_VERSION, GET_RS_SCHEMA, DATA
from indy_node.server.request_handlers.domain_req_handlers.rs_schema_handler import RsSchemaHandler
from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.common.request import Request
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.read_request_handler import ReadRequestHandler


class GetSchemaHandler(ReadRequestHandler):

    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager, GET_RS_SCHEMA, DOMAIN_LEDGER_ID)

    def get_result(self, request: Request):
        self._validate_request_type(request)
        assert request.operation[RS_SCHEMA_ID] is not None
        schema_id = request.operation[RS_SCHEMA_ID]
        did, _, schema_type, label, version = schema_id.split(":")
        path = RsSchemaHandler.make_state_path(did, schema_type, label, version)
        schema, last_seq_no, last_update_time, proof = self.get_schema(path_key=path, with_proof=True)
        if schema is None:
            schema = {}
        schema.update({
            RS_SCHEMA_LABEL: label,
            RS_SCHEMA_VERSION: version
        })
        return self.make_result(request=request,
                                data=schema,
                                last_seq_no=last_seq_no,
                                update_time=last_update_time,
                                proof=proof)

    def get_schema(self,
                   path_key: str,
                   is_committed=True,
                   with_proof=True) -> (str, int, int, list):
        assert path_key is not None
        try:
            keys, seq_no, last_update_time, proof = self.lookup(path_key, is_committed, with_proof=with_proof)
            return keys, seq_no, last_update_time, proof
        except KeyError:
            return None, None, None, None
