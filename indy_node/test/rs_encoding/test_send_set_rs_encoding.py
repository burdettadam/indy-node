import asyncio
import json

from indy.ledger import sign_request, submit_request

from indy_common.constants import RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, RS_JSON_LD_ID, \
    RS_META_ID, RS_META_TYPE, SET_RS_ENCODING
from indy_common.state.state_constants import MARKER_RS_ENCODING
from plenum.test.helper import sdk_check_reply, sdk_sign_and_submit_req, sdk_get_and_check_replies


def test_send_encoding(looper, sdk_pool_handle, sdk_wallet_endorser):
    _, requests_did = sdk_wallet_endorser
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
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_endorser, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    assert rep[0][1]['result']['txnMetadata']['txnId']
