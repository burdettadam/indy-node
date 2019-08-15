from indy_common.constants import CONTEXT_NAME, CONTEXT_VERSION, GET_CONTEXT
from indy_common.req_utils import get_read_context_id, get_read_context_name, get_read_context_version
from indy_node.server.request_handlers.domain_req_handlers.context_handler import make_state_path_for_context
from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.common.request import Request
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.read_request_handler import ReadRequestHandler


class GetContextHandler(ReadRequestHandler):

    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager, GET_CONTEXT, DOMAIN_LEDGER_ID)

    def get_result(self, request: Request):
        self._validate_request_type(request)
        context_id = get_read_context_id(request)
        context, last_seq_no, last_update_time, proof = self.get_context(
            identifier=context_id,
            with_proof=True
        )
        if context is None:
            context = {}
        context.update({
            CONTEXT_NAME: context_name,
            CONTEXT_VERSION: context_version
        })
        return self.make_result(request=request,
                                data=context,
                                last_seq_no=last_seq_no,
                                update_time=last_update_time,
                                proof=proof)

    def get_context(self,
                    identifier: str,
                    is_committed=True,
                    with_proof=True) -> (str, int, int, list):
        assert identifier is not None
        try:
            keys, seq_no, last_update_time, proof = self.lookup(identifier, is_committed, with_proof=with_proof)
            return keys, seq_no, last_update_time, proof
        except KeyError:
            return None, None, None, None
