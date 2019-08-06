import json

import pytest

from indy_node.server.request_handlers.domain_req_handlers.rs_mapping_handler import RsMappingHandler


def test_validate_rs_mapping_fail_on_empty():
    with pytest.raises(Exception):
        RsMappingHandler._validate_context({})


def test_validate_rs_mapping_fail_no_context_property():
    input_dict = {}
    with pytest.raises(Exception):
        RsMappingHandler._validate_context(input_dict)

