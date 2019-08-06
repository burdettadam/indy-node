{
  "@context": "ctx:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
  "@id": "sch:sov:Q6kuSqnxE57waPFs2xAs7q:2:ISO18013_Drivers_License:1.0",
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

{
  "@context": [
    "ctx:sov:sch:v1",
    "ctx:sov:3FtTB4kzSyApkyJ6hEEtxNH4H"
  ],
  "@id": "sch:sov:35qJWkTM7znKnicY7dq5Y",
  "@type": "rdfs:Class",
  "rdfs:comment": "A driver is a person licensed to operate a vehicle.",
  "rdfs:label": "Driver",
  "rdfs:subClassOf": {
    "@id": "Person"
  },
  "rdfs_properties": [
    {
      "@id": "driver:portrait",
      "@type": "rdf:property",
      "rdfs:label": {
        "en": "Portrait"
      },
      "rdfs:comment": {
        "en": "The license holder's portrait."
      },
      "rdfs:domain": "driver:Driver",
      "rdfs:range": "ImageObject"
    },
    {
      "@id": "driver:signature",
      "@type": "rdf:property",
      "rdfs:label": {
        "en": "Signature"
      },
      "rdfs:comment": {
        "en": "A picture of the license holder's signature."
      },
      "rdfs:domain": "driver:Driver",
      "rdfs:range": "ImageObject"
    },
    {
      "@id": "driver:eyeColor",
      "@type": "rdf:property",
      "rdfs:label": {
        "en": "Eye Color"
      },
      "rdfs:comment": {
        "en": "The license holder's eye color."
      },
      "rdfs:domain": "driver:Driver",
      "rdfs:range": "Text"
    },
    {
      "@id": "driver:hairColor",
      "@type": "rdf:property",
      "rdfs:label": {
        "en": "Hair Color"
      },
      "rdfs:comment": {
        "en": "The license holder's hair color."
      },
      "rdfs:domain": "driver:Driver",
      "rdfs:range": "Text"
    },
    {
      "@id": "driver:restriction",
      "@type": "rdf:property",
      "rdfs:label": {
        "en": "Restrictions"
      },
      "rdfs:comment": {
        "en": "Restrictions on the license holder."
      },
      "rdfs:domain": "driver:Driver",
      "rdfs:range": "Text"
    }
  ]
}
