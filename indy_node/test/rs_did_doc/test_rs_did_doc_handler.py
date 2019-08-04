import json

import pytest

from indy_node.server.request_handlers.domain_req_handlers.rs_did_doc_handler import RsDidDocHandler


def test_validate_rs_cred_def_fail_on_empty():
    with pytest.raises(Exception):
        RsDidDocHandler._validate_context({})


def test_validate_rs_cred_def_fail_no_context_property():
    input_dict = {}
    with pytest.raises(Exception):
        RsDidDocHandler._validate_context(input_dict)

