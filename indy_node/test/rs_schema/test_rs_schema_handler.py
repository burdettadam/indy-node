import json

import pytest

from indy_common.constants import RS_SCHEMA_TYPE, RS_SCHEMA_CONTEXT, RS_SCHEMA_DOCUMENT, RS_META_NAME, RS_META_VERSION
from indy_node.server.request_handlers.domain_req_handlers.rs_schema_handler import RsSchemaHandler


def test_validate_rs_schema_fail_on_empty():
    with pytest.raises(Exception):
        RsSchemaHandler._validate({}, {})


def test_validate_rs_schema():
    with pytest.raises(Exception):
        RsSchemaHandler._validate({
            RS_META_NAME: "ISO18013_Drivers_License",
            RS_META_VERSION: "1.0"
        }, {
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
            },
            "administrativeNumber": "Text"})