from indy_common.constants import GET_RS_SCHEMA, RS_META, RS_META_ID
from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.common.request import Request
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.read_request_handler import ReadRequestHandler


class GetRsSchemaHandler(ReadRequestHandler):
    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager, GET_RS_SCHEMA, DOMAIN_LEDGER_ID)

    def get_result(self, request: Request):
        self._validate_request_type(request)
        _id = request.operation[RS_META][RS_META_ID]
        _did, _rs_schema_type, _type, _label, _version = _id.split(":")
        if not _id:
            pass  # TODO: raise error if no id is passed.
        schema, last_seq_no, last_update_time, proof = self.get_schema(path_key=_id,)
        if schema is None:
            schema = {}
        return self.make_result(request=request, data=schema, last_seq_no=last_seq_no, update_time=last_update_time,
                                proof=proof)

    def get_schema(self, path_key: str, is_committed=True, with_proof=True) -> (str, int, int, list):
        if path_key is None:
            pass
        try:  # this returns: keys, seq_no, last_update_time, proof
            return self.lookup(path_key, is_committed, with_proof=with_proof)
        except KeyError:
            return None, None, None, None
