import json

import pytest

from indy_common.constants import RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, \
    RS_META_ID, RS_META_TYPE, RS_JSON_LD_ID, SET_RS_ENCODING, GET_RS_ENCODING
from indy_common.state.state_constants import MARKER_RS_SCHEMA, MARKER_RS_ENCODING

from indy_node.test.helper import createUuidIdentifier, modify_field
from indy.ledger import submit_request, sign_and_submit_request, sign_request

from plenum.test.helper import sdk_check_reply, sdk_sign_and_submit_req, sdk_get_and_check_replies, sdk_send_and_check


@pytest.fixture(scope="module")
def write_encoding(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee):
    _, requests_did = sdk_wallet_trustee
    authors_did, name, version, type = requests_did, "ISO18023_Drivers_License", "1.1", MARKER_RS_ENCODING
    _id = authors_did + ':' + type + ':' + name + ':' + version
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_ENCODING,
            RS_META: {
                RS_META_ID: _id,
                RS_META_TYPE: MARKER_RS_ENCODING,
                RS_META_NAME: name,
                RS_META_VERSION: version
            },
            RS_DATA: {
                RS_JSON_LD_ID: _id,
                'meta': {
                    'discription': 'this is a test encoding',
                    'label': 'asdfasdfasdf',
                    'source': 'did.example.com'
                },
                'test_vectors': {
                    'simple': {
                        'input': 'YOLO',
                        'output': 123456
                    }
                },
                'pseudo_code': 'just output 123456'
            }
        },
        "identifier": authors_did,
        "reqId": 1565971763281198952,
        "protocolVersion": 2
    })
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_trustee, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    txn_id = rep[0][1]['result']['txnMetadata']['txnId']
    return txn_id


def test_get_schema_succeeds(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee, write_encoding):
    _, requests_did = sdk_wallet_trustee
    authors_did = requests_did
    txn_json = json.dumps({
        'operation': {
            'type': GET_RS_ENCODING,
            RS_META: {
                RS_META_ID: write_encoding
            },
            "identifier": authors_did,
            "reqId": 1555971763281198952,
            "protocolVersion": 2
        }})
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_trustee, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    assert rep[1]['result']['seqNo']
