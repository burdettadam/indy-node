import asyncio
import json

from indy.ledger import sign_request, submit_request

from indy_common.constants import SET_RS_SCHEMA, RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, RS_JSON_LD_ID, \
    RS_META_ID, RS_META_TYPE
from indy_common.state.state_constants import MARKER_RS_SCHEMA
from plenum.test.conftest import sdk_wallet_trustee
from plenum.test.helper import sdk_check_reply, sdk_sign_and_submit_req, sdk_get_and_check_replies


def test_send_schema(looper, sdk_pool_handle, sdk_wallet_endorser):
    _, requests_did = sdk_wallet_endorser
    authors_did, name, version, type = requests_did, "ISO18023_Drivers_License", "1.1", MARKER_RS_SCHEMA
    _id = authors_did + ':' + type + ':' + name + ':' + version
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_SCHEMA,
            RS_META: {
                RS_META_ID: _id,
                RS_META_TYPE: MARKER_RS_SCHEMA,
                RS_META_NAME: name,
                RS_META_VERSION: version
            },
            RS_DATA: {
                RS_JSON_LD_ID: _id,
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
