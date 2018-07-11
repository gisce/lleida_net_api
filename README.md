# Lleida.net Click & Sign client

It provides a Python client desired to interact with Lleida.net Click & Sign API.

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
from lleida_net.click_sign import Client
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

