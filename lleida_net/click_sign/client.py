# -*- coding: utf-8 -*-

from .api import CS_API
from . import serializers as schema
import os


class Signature(object):
    def __init__(self, api):
        self.session = api

    def start(self):
        pass

class Client(object):
    def __init__(self, user=None, password=None, environment=None):

        # Handle the user
        self.user = user
        if not user:
            self.user = os.getenv('CS_user')
        assert self.user, "The user is needed to initialize the Lleida.net Click'n'Sign connection"

        # Handle the password
        self.password = password
        if not password:
            self.password = os.getenv('CS_password')
        assert self.password, "The password is needed to initialize the Lleida.net Click'n'Sign connection"

        # Handle the env, by default prod
        self.environment = "prod"
        if environment:
            self.environment = environment

        self.API = CS_API(user=self.user, password=self.password, environment=self.environment)

        # Prepare API resources
        self.signature = Signature(self.API)
