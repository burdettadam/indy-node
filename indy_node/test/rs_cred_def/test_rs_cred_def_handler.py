import json

import pytest

from indy_node.server.request_handlers.domain_req_handlers.rs_cred_def_handler import RsCredDefHandler


def test_validate_rs_cred_def_fail_on_empty():
    with pytest.raises(Exception):
        RsCredDefHandler._validate_context({})


def test_validate_rs_cred_def_fail_no_context_property():
    input_dict = {}
    with pytest.raises(Exception):
        RsCredDefHandler._validate_context(input_dict)

