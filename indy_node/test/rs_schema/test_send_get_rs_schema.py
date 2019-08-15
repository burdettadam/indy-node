import json

import pytest

from indy_common.constants import GET_RS_SCHEMA, SET_RS_SCHEMA, RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, \
    RS_META_ID
from indy_common.state.state_constants import MARKER_RS_SCHEMA

from indy_node.test.api.helper import write_txn
from indy_node.test.helper import createUuidIdentifier, modify_field
from indy.ledger import submit_request, sign_and_submit_request, sign_request

from plenum.test.helper import sdk_check_reply


@pytest.fixture(scope="module")
def write_schema(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee):
    _, authors_did = sdk_wallet_trustee
    name, version = "ISO18013_DriverLicenseContext", "1.9"
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_SCHEMA,
            RS_META: {
                RS_META_NAME: "ISO18013_Drivers_License",
                RS_META_VERSION: "1.0"
            },
            RS_DATA: {
                "@context": "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
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
                }
            },
            "identifier": authors_did,
            "reqId": 12345678,
            "protocolVersion": 2
        }
    })
    path_dict = {id: authors_did + ':' + MARKER_RS_SCHEMA + ':' + name + ':' + version}
    _json, _ = write_txn(looper, sdk_pool_handle, sdk_wallet_trustee, txn_json, path_dict, sign=True, check=True)
    return json.loads(_json)['id']


@pytest.fixture(scope="module")
def send_schema_req(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee):
    _, requests_did = sdk_wallet_trustee
    authors_did = requests_did
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_SCHEMA,
            RS_META: {
                RS_META_NAME: "ISO18023_Drivers_License",
                RS_META_VERSION: "1.1"
            },
            RS_DATA: {
                "@context": "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
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
                }
            },
            "identifier": authors_did,
            "reqId": 13345678,
            "protocolVersion": 2
        }
    })
    sign_txn_json = sign_request(sdk_wallet_trustee, authors_did, txn_json)
    rep = submit_request(sdk_pool_handle, sign_txn_json)
    return txn_json, rep


def test_get_schema_succeeds(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee, write_schema):
    _, requests_did = sdk_wallet_trustee
    authors_did = requests_did
    txn_json = json.dumps({
        'operation': {
            'type': GET_RS_SCHEMA,
            RS_META: {
                RS_META_ID: authors_did + ':' + MARKER_RS_SCHEMA + ':' + 'ISO18013_DriverLicenseContext' + ':' + '1.9'
            },
            "identifier": authors_did,
            "reqId": 12365978,
            "protocolVersion": 2
        }})
    #rep = submit_request(sdk_pool_handle, txn_json)
    rep = sdk_check_reply(submit_request(sdk_pool_handle, txn_json))  # do we need this check?
    assert rep[1]['result']['seqNo']
