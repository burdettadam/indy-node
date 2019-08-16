import asyncio
import json

from indy.ledger import sign_request, submit_request

from indy_common.constants import SET_RS_SCHEMA, RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA
from plenum.test.conftest import sdk_wallet_trustee
from plenum.test.helper import sdk_check_reply, sdk_sign_and_submit_req, sdk_get_and_check_replies


def test_send_schema(looper, sdk_pool_handle, sdk_wallet_endorser):
    _, requests_did = sdk_wallet_endorser
    authors_did = requests_did
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_SCHEMA,
            RS_META: {
                RS_META_NAME: "ISO18023_Drivers_License",
                RS_META_VERSION: "1.1"
            },
            RS_DATA: {
                "@context": "ctx:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
                "@type": "rdfs:Class",
                "rdfs:comment": "ISO18013 International Driver License",
                "rdfs:label": "Driver License",
                "rdfs:subClassOf": {
                    "@id": "sch:Thing"
                },
                "driver": "Driver",
                "dateOfIssue": "Date",
                "dateOfExpiry": "Date",
                "issuingAuthority": "Text",
                "licenseNumber": "Text",
                "categoriesOfVehicles": {
                    "vehicleType": "Text",
                    "vehicleType-input": {
                        "@type": "sch:PropertyValueSpecification",
                        "valuePattern": "^(A|B|C|D|BE|CE|DE|AM|A1|A2|B1|C1|D1|C1E|D1E)$"
                    },
                    "dateOfIssue": "Date",
                    "dateOfExpiry": "Date",
                    "restrictions": "Text",
                    "restrictions-input": {
                        "@type": "sch:PropertyValueSpecification",
                        "valuePattern": "^([A-Z]|[1-9])$"
                    }
                },
                "administrativeNumber": "Text"
            }

        },
        "identifier": authors_did,
        "reqId": 1565971763281198952,
        "protocolVersion": 2
    })
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_endorser, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])

    # sign_txn_json = asyncio.ensure_future(sign_request(sdk_wallet_trustee, authors_did, txn_json))
    # sdk_check_reply(asyncio.ensure_future(submit_request(sdk_pool_handle, sign_txn_json)))
