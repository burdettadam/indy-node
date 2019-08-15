import json

import pytest
from plenum.common.exceptions import RequestNackedException

from plenum.common.constants import DATA, NAME, VERSION, TXN_METADATA, TXN_METADATA_SEQ_NO

from plenum.common.types import OPERATION

from plenum.test.helper import sdk_sign_and_submit_req, sdk_get_and_check_replies

from indy_node.test.api.helper import write_encoding
from indy_node.test.helper import createUuidIdentifier, modify_field


@pytest.fixture(scope="module")
def send_mapping(looper, sdk_pool_handle, nodeSet, sdk_wallet_trustee):
    context_json, _ = write_encoding(looper, sdk_pool_handle, sdk_wallet_trustee,
                {
            "@context": {
                "referenceNumber": "https://example.com/vocab#referenceNumber",
                "favoriteFood": "https://example.com/vocab#favoriteFood"
            }
        },
        "ISO18013_DriverLicenseMapping",
        "1.9")
    return json.loads(context_json)['id']
