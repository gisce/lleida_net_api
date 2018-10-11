from __future__ import (division, absolute_import, print_function, unicode_literals)

from six.moves import urllib


import os
import base64

from lleida_net.click_sign import Client, NotValidSignatureSchemaException
from marshmallow import pprint

import logging
logging.basicConfig(level=logging.DEBUG)

ATTACHMENTS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../specs/attachments"

config = {
    'user': 'USER',
    'password': 'PASSWORD',
    'environment': 'prod'
}
client = Client(**config)

with open(ATTACHMENTS_PATH + "/dummy.pdf", "rb") as pdf:
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
