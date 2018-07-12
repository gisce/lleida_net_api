import os
import base64
import urllib.parse

from lleida_net.click_sign import Client, NotValidSignatureSchemaException
from marshmallow import pprint

import logging
logging.basicConfig(level=logging.DEBUG)

ATTACHMENTS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../specs/attachments"

client = Client()

with open(ATTACHMENTS_PATH + "/contract.pdf", "rb") as pdf:
    encoded_pdf = urllib.parse.quote_plus(base64.b64encode(pdf.read()))

data = {
    "config_id": 478,
    "contract_id": "1004455512",
    "level": [
        {
            "level_order": 0,
            "signatories": [
                {
                    "phone": "+34666666666",
                    "email": "here@iam.net",
                    "name": "Rolf",
                    "surname": "Laurent"
                },
            ]
        },
    ],
    "file": [
        {
            "filename": "Contract_1004455512.pdf",
            "content": encoded_pdf,
            "file_group": "contract_files"
        }
    ]
}

response = client.signature.start(data)
pprint (response, indent=4)
