import json

import pytest

from indy_node.server.request_handlers.domain_req_handlers.rs_encoding_handler import RsEncodingHandler


def test_validate_encoding_fail_on_empty():
    with pytest.raises(Exception):
        RsEncodingHandler._validate({})


def test_validate_encoding():
    input_dict = {}
    with pytest.raises(Exception):
        RsEncodingHandler._validate(input_dict)

