import json

import pytest

from indy_common.constants import RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, \
    RS_META_ID, RS_META_TYPE, RS_JSON_LD_ID, SET_RS_MAPPING, GET_RS_MAPPING
from indy_common.state.state_constants import MARKER_RS_MAPPING
from plenum.test.helper import sdk_sign_and_submit_req, sdk_get_and_check_replies


@pytest.fixture(scope="module")
def write_mapping(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee):
    _, requests_did = sdk_wallet_trustee
    authors_did, name, version, type = requests_did, "ISO18023_Drivers_License", "1.1", MARKER_RS_MAPPING
    _id = authors_did + ':' + type + ':' + name + ':' + version
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_MAPPING,
            RS_META: {
                RS_META_ID: _id,
                RS_META_TYPE: MARKER_RS_MAPPING,
                RS_META_NAME: name,
                RS_META_VERSION: version
            },
            RS_DATA: {
                RS_JSON_LD_ID: _id,
                "@context": [
                    "https://w3.org/2018/credentials/v1",
                    "ctx:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
                    "ctx:sov:map:v1",
                    "ctx:sov:enc:v1",
                    {
                        "UTF-8_SHA-256": "enc:sov:49ob1bkSq415i3m2NhkczAjJMN77F",
                        "DateRFC3339_SecondsSince1970": "enc:sov:AE3wtUQn6EUA5sfZSHij7B",
                        "DateRFC3339_DaysSince1900": "enc:sov:UWsJwJaSmaQMFkqbc1khGmtoT"
                    }
                ],
                "@type": [
                    "sch:sov:86hgxTA9dRAvvyMNe4sQYAxuh1Jk4"
                ],
                "contexts": [
                    "https://w3.org/2018/credentials/v1",
                    "ctx:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD"
                ],
                "schemas": [
                    "VerifiableCredential",
                    "AnonCred",
                    "sch:sov:86hgxTA9dRAvvyMNe4sQYAxuh1Jk4"
                ],
                "attributeMap": {
                    "a1": {
                        "graphPath": {
                            "@list":
                                [
                                    "https://w3.org/2018/credentials/v1/VerifiableCredential/issuer"
                                ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a2": {
                        "graphPath": {
                            "@list": [
                                "https://w3.org/2018/credentials/v1/VerifiableCredential/issuanceDate"
                            ]
                        },
                        "encoding": "DateRFC3339_SecondsSince1970"
                    },
                    "a3": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "familyName"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a4": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "givenName"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a5": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "birthDate"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a6": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "birthPlace",
                                "address",
                                "addressRegion"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a7": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "address",
                                "streetAddress"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a8": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "address",
                                "addressLocality"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a9": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "address",
                                "addressRegion"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a10": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "address",
                                "postalCode"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a11": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "gender"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a12": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "height",
                                "value"
                            ]
                        },
                        "encoding": "HeightISO18013_HeightInInches"
                    },
                    "a13": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "weight",
                                "value"
                            ]
                        },
                        "encoding": "Integer_Integer"
                    },
                    "a14": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "portrait"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a15": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "signature"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a16": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "eyeColor"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a17": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "hairColor"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a18": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "Driver",
                                "restrictions"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a19": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "dateOfIssue"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a20": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "dateOfExpiry"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a21": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "issuingAuthority"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a22": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "licenseNumber"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a23": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[0]",
                                "type"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a24": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[0]",
                                "dateOfIssue"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a25": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[0]",
                                "dateOfExpiry"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a26": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[0]",
                                "restrictions"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a27": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[1]",
                                "type"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a28": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[1]",
                                "dateOfIssue"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a29": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[1]",
                                "dateOfExpiry"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a30": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[1]",
                                "restrictions"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a31": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[2]",
                                "type"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a32": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[2]",
                                "dateOfIssue"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a33": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[2]",
                                "dateOfExpiry"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a34": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[2]",
                                "restrictions"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a35": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[3]",
                                "type"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a36": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[3]",
                                "dateOfIssue"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a37": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[3]",
                                "dateOfExpiry"
                            ]
                        },
                        "encoding": "DateRFC3339_DaysSince1900"
                    },
                    "a38": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "categoriesOfVehicles[3]",
                                "restrictions"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    },
                    "a39": {
                        "graphPath": {
                            "@list": [
                                "DriverLicense",
                                "administrativenumber"
                            ]
                        },
                        "encoding": "UTF-8_SHA-256"
                    }
                }
            }
        },
        "identifier": authors_did,
        "reqId": 1565971763481198952,
        "protocolVersion": 2
    })
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_trustee, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    assert rep[0][1]['result']['txnMetadata']['txnId']


def test_get_mapping_succeeds(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee, write_mapping):
    _, requests_did = sdk_wallet_trustee
    authors_did = requests_did
    txn_json = json.dumps({
        'operation': {
            'type': GET_RS_MAPPING,
            RS_META: {
                RS_META_ID: write_mapping
            },
            "identifier": authors_did,
            "reqId": 12345678,
            "protocolVersion": 2
        }})
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_trustee, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    assert rep[1]['result']['seqNo']
