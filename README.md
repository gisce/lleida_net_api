# Lleida.net Click & Sign and SMS client

It provides a Python client desired to interact with Lleida.net Click & Sign API and SMS API.

## Usage

Simply configure the `USER` and the `PASSWORD` as exported environment vars, or attach it at Client initialization time

### ENV vars

Just define the needed ENV vars:
```
$ export CS_USER=my_username
$ export CS_PASSWORD=my_password

```

, and instantiate the Client without any parameter:

```
# Click & Sign API
from lleida_net.click_sign import Client
client = Client()

# SMS API
from lleida_net.sms import Client
client = Client()
```

### Passed config

Instantiate the Client passing the key and secret oauth tokens:
```
from lleida_net.click_sign import Client

config = {
    'user': "my_username",
    'password': "my_password",
}

client = Client(**config)
```

## Available sections

- [Signature](#signature)
- [SMS](#sms)

### Signature

Section desired to manage the Signatures.

Available methods:

- [start](#signaturestart)
- [status](#signaturestatus)

#### Signature.Start

```
encoded_pdf = base64.b64encode(a_pdf.read())

data = {
    "config_id": 1,
    "contract_id": "ContractID",
    "level": [
        {
            "level_order": 0,
            "signatories": [
                {
                    "phone": "+34666666666",
                    "email": "here@iam.com",
                    "name": "MyName",
                    "surname": "MySurname"
                },
            ]
        },
    ],
    "file": [
        {
            "filename": "contract.pdf",
            "content": encoded_pdf,
            "file_group": "contract_files"
        }
    ]
}

self.client.signature.start(data)
```


#### Signature.Status

It tries to reach the status of an already started signature.

If not, raises an exception

```
print (self.client.signature.status(signatory_id=555))

{'signatory_email': 'xtorello@gisce.net', 'signatory_status': '6', 'signatory_status_date': '1540284984', 'signatory_id': 555}


print (self.client.signature.status(signatory_id=-1))
NotFoundSignatureException
```

### SMS

#### Send SMS

```
from lleida_net.sms import Client                                                            
config = {                                                                                   
    'user': "my_user",                                                                
    'password': "my_pass",                                                                
}                                                                                            
c = Client(**config)                                                                         
headers = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
                                                                                             
resposta = c.API.post(resource='',json={                                                     
    "sms": {                                                                                 
        "txt": "My sms message text",                                                                  
        "dst": {                                                                             
            "num": "+34600000000"                                                            
        },                                                                                   
        "src": "Your company name"                                                                 
    }                                                                                        
}, headers=headers)                                                                          
```

#### Response

```
resposta.result                                                                              
{u'code': 200, u'newcredit': 93.0, u'request': u'sms', u'status': u'Success'}                
```

#### SMS API key mode (optional)

The legacy `Client(user, password)` behavior remains unchanged. API key
authentication, explicit timeouts and error payload preservation are opt-in:

```python
from lleida_net.sms import Client

client = Client(
    user='my_user',
    password='my_api_key',
    api_key='my_api_key',
    api_url='https://api.lleida.net/sms/v2/',
    timeout=15,
    preserve_error_response=True,
    capture_transport_errors=True,
)
```

When `api_key` is provided, the client sends `Authorization: x-api-key ...`
and no longer injects `password` into the SMS document. Existing callers that
do not provide the new arguments keep the 0.6.2 request and response behavior.
With `capture_transport_errors=True`, timeouts, request failures and invalid
JSON responses are returned as error results with a `transport_error` value;
without it, those exceptions keep being raised as in 0.6.2.
