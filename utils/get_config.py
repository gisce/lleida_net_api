import os
from lleida_net.click_sign import Client
from marshmallow import pprint

import logging
logging.basicConfig(level=logging.DEBUG)

CONFIG_TO_GET = "Button signature"

# Prepare a client using ENV credentials
client = Client()

# Fetch all available
response = client.configuration.get_config_list()
config_id_list = {a_config.config_id: a_config.name for a_config in response.config}
config_id = [a_config.config_id for a_config in response.config if a_config.name == CONFIG_TO_GET][0]
print (config_id_list)


## Fetch config details
print ("Fetching config details for '{}'".format(config_id))
response = client.configuration.get_config(config_id)
# pprint (response, indent=2)
