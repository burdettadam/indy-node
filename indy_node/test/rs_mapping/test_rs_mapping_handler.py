import json

import pytest

from indy_node.server.request_handlers.domain_req_handlers.rs_mapping_handler import RsMappingHandler


def test_validate_rs_mapping_fail_on_empty():
    with pytest.raises(Exception):
        RsMappingHandler._validate({})


def test_validate_rs_mapping():
    input_dict = {}
    with pytest.raises(Exception):
        RsMappingHandler._validate(input_dict)

