import os
from lleida_net.click_sign import Client
from marshmallow import pprint

import logging
logging.basicConfig(level=logging.DEBUG)

# Prepare a client using ENV credentials
client = Client()

logo = ""

to_change = {
    'auto_cancel':'N',
    'color_background':'',
    'color_button_background':'#AEDE00',
    'color_button_text':'#FFFFFF',
    'color_text':'',
    'default_email_from_name':'My Company',
    'default_sms_sender':'Click&Sign',
    'email':[
        {
            'attachment_file_group':[
            ],
            'bcc':'',
            'body_free_text':'',
            'body_template':'',
            'cc':'',
            'registered':'Y',
            'reminder_lapse':'0',
            'subject':'Firma digital del contrato',
            'to':'SIGNATORY',
            'type':'start'
        },
        {
            'attachment_file_group':[
                'SIGNATORY_STAMP',
                'SIGNATORY_EVIDENCE'
            ],
            'bcc':'',
            'body_free_text':'',
            'body_template':'',
            'cc':'',
            'registered':'N',
            'reminder_lapse':'0',
            'subject':'¡Felicidades! El contrato ha sido firmado correctamente.',
            'to':'SIGNATORY',
            'type':'signed'
        },
        {
            'attachment_file_group':[

            ],
            'bcc':'',
            'body_free_text':'En breve recibirá sus credenciales de acceso a la Oficina Virtual.',
            'body_template':'',
            'cc':'',
            'registered':'N',
            'reminder_lapse':'0',
            'subject':'¡Felicidades! El contrato ha sido firmado correctamente.',
            'to':'SIGNATORY',
            'type':'end_ok'
        },
        {
            'attachment_file_group':[

            ],
            'bcc':'',
            'body_free_text':'En breve recibirá sus credenciales de acceso a la Oficina Virtual.',
            'body_template':'',
            'cc':'',
            'registered':'N',
            'reminder_lapse':'0',
            'subject':'No ha sido posible firmar el contrato',
            'to':'SIGNATORY',
            'type':'end_ko'
        },
        {
            'attachment_file_group':[

            ],
            'bcc':'',
            'body_free_text':'',
            'body_template':'',
            'cc':'',
            'registered':'N',
            'reminder_lapse':'0',
            'subject':'El contrato para firmar ha expirado',
            'to':'SIGNATORY',
            'type':'expired'
        }
    ],
    'expire_lapse': 720,
    'landing':{
        'landing_template':'',
        'signature_on_sign_required_elements':{
            'handwritten':'N',
            'otp':'N',
            'otp_length':6,
            'otp_max_retries':3,
            'otp_sending':'on_landing'
        },
        'signature_type':'on_sign'
    },
    'lang':'ES',
    'logo':logo,
    'name':'Button signature',
    'registered_company_name':'MyCompany S.L.',
    'registered_company_vat_number':'VAT',
    'registered_langs':'ES',
    'signature_cb_url':'',
    'sms':[

    ],
    'status':'enabled'
}

response = client.configuration.set_config(to_change)
pprint (response, indent=4)
