import asyncio
import json

from indy.ledger import sign_request, submit_request

from indy_common.constants import RS_META, RS_META_NAME, RS_META_VERSION, RS_DATA, RS_JSON_LD_ID, \
    RS_META_ID, RS_META_TYPE, SET_RS_DID_DOC
from indy_common.state.state_constants import MARKER_RS_DID_DOC
from plenum.test.conftest import sdk_wallet_trustee
from plenum.test.helper import sdk_check_reply, sdk_sign_and_submit_req, sdk_get_and_check_replies


def test_send_did_doc(looper, sdk_pool_handle, sdk_wallet_endorser):
    _, requests_did = sdk_wallet_endorser
    authors_did, name, version, type = requests_did, "ISO18023_Drivers_License", "1.1", MARKER_RS_DID_DOC
    _id = authors_did + ':' + type + ':' + name + ':' + version
    txn_json = json.dumps({
        'operation': {
            'type': SET_RS_DID_DOC,
            RS_META: {
                RS_META_ID: _id,
                RS_META_TYPE: MARKER_RS_DID_DOC,
                RS_META_NAME: name,
                RS_META_VERSION: version
            },
            RS_DATA: {
                RS_JSON_LD_ID: _id,
                '@context': 'https://w3id.org/future-method/v1',
                'publicKey': [
                    {
                        'id': 'did:example:123456789abcdefghi#keys-1',
                        'type': 'RsaVerificationKey2018',
                        'controller': 'did:example:123456789abcdefghi',
                        'publicKeyPem': '-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#keys-3',
                        'type': 'Ieee2410VerificationKey2018',
                        'controller': 'did:example:123456789abcdefghi',
                        'publicKeyPem': '-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n'
                    }
                ],
                'authentication': [
                    'did:example:123456789abcdefghi#keys-1',
                    'did:example:123456789abcdefghi#keys-3',
                    {
                        'id': 'did:example:123456789abcdefghi#keys-2',
                        'type': 'Ed25519VerificationKey2018',
                        'controller': 'did:example:123456789abcdefghi',
                        'publicKeyBase58': 'H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV'
                    }
                ],
                'service': [
                    {
                        'id': 'did:example:123456789abcdefghi#oidc',
                        'type': 'OpenIdConnectVersion1.0Service',
                        'serviceEndpoint': 'https://openid.example.com/'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#vcStore',
                        'type': 'CredentialRepositoryService',
                        'serviceEndpoint': 'https://repository.example.com/service/8377464'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#xdi',
                        'type': 'XdiService',
                        'serviceEndpoint': 'https://xdi.example.com/8377464'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#hub',
                        'type': 'HubService',
                        'serviceEndpoint': 'https://hub.example.com/.identity/did:example:0123456789abcdef/'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#messaging',
                        'type': 'MessagingService',
                        'serviceEndpoint': 'https://example.com/messages/8377464'
                    },
                    {
                        'type': 'SocialWebInboxService',
                        'id': 'did:example:123456789abcdefghi#inbox',
                        'serviceEndpoint': 'https://social.example.com/83hfh37dj',
                        'description': 'My public social inbox',
                        'spamCost': {
                            'amount': '0.50',
                            'currency': 'USD'
                        }
                    },
                    {
                        'type': 'DidAuthPushModeVersion1',
                        'id': 'did:example:123456789abcdefghi#push',
                        'serviceEndpoint': 'http://auth.example.com/did:example:123456789abcdefghi'
                    },
                    {
                        'id': 'did:example:123456789abcdefghi#bops',
                        'type': 'BopsService',
                        'serviceEndpoint': 'https://bops.example.com/enterprise/'
                    }
                ],
                'proof': [{
                    'type': 'LinkedDataSignature2015',
                    'created': '2016-02-08T16:02:20Z',
                    'creator': 'did:example:8uQhQMGzWxR8vw5P3UWH1ja#keys-1',
                    'signatureValue': 'QNB13Y7Q9...1tzjn4w=='
                }]
            }
        },
        'identifier': authors_did,
        'reqId': 1565971763281198952,
        'protocolVersion': 2
    })
    req = sdk_sign_and_submit_req(sdk_pool_handle, sdk_wallet_endorser, txn_json)
    rep = sdk_get_and_check_replies(looper, [req])
    assert rep[0][1]['result']['txnMetadata']['txnId']
