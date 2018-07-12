# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
import io
from munch import Munch

import logging
logging.basicConfig(level=logging.DEBUG)

from lleida_net.click_sign import CS_API, serializers

fixtures_path = 'specs/fixtures/api/'

spec_VCR = vcr.VCR(
    record_mode='new',
    cassette_library_dir=fixtures_path
)

config = {
    'user': 'user',
    'password': 'password',
    'environment': 'prod'
}

scope = {
    "get_config": {
        "url": "/get_config"
    }
}

with description('A new CS API'):
    with before.each:
        with spec_VCR.use_cassette('init.yaml'):
            self.config = config
            self.api = CS_API(**config)

    with context('initialization'):
        with it('must be performed as expected'):
            with spec_VCR.use_cassette('init.yaml'):
                assert type(self.api.user) == str, "User format is not the expected (str)"
                assert self.api.user == self.config['user'], "User is not the expected one"

                assert type(self.api.password) == str, "Password format is not the expected (str)"
                assert self.api.password == self.config['password'], "Password is not the expected one"

                assert type(self.api.environment) == str, "Environment format is not the expected (str)"
                assert self.api.environment == self.config['environment'], "Environment is not the expected one"

        with it('must be performed as expected for errors'):
            with spec_VCR.use_cassette('init.yaml'):
                config = {
                    'user': 'unnamed',
                    'password': 'unnamed',
                }
                self.api = CS_API(**config)
                response = self.api.post("get_config_list")
                assert response.error, "It must return an error for incorrect logins"


    with context('config fetch'):
        with it('must work as expected'):
            with spec_VCR.use_cassette('get_config_list.yaml'):
                response = self.api.post("get_config_list")
                validate = serializers.ResponseSchema().load(response.result)

                assert not validate.errors, "There must be no errors while validating API response"

                assert not response.error, "Response must not contain errors"
                assert response.code == 200, "Response code must be 200"
                assert "result" in response, "A 'result' must be inside the response"
                result = Munch(response.result)
                assert "config" in result, "A 'config' must be inside the result'"
                config = result.config
                assert type(config) == list, "Config must be a list of configurations"
