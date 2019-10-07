# -*- coding: utf-8 -*-

# Automatic provisioning of AWS S3 buckets.

import time
import botocore
import boto3
import json
import nixops.util
import nixops.resources
import nixops.ec2_utils
import requests
from xml.etree import ElementTree


class saasAuthDefinition(nixops.resources.ResourceDefinition):

    @classmethod
    def get_type(cls):
        return "saas-auth"

    @classmethod
    def get_resource_type(cls):
        return "saasAuths"

    def __init__(self, xml, config={}):
        nixops.resources.ResourceDefinition.__init__(self, xml, config)
        self.deployment_name = xml.find(
            "attrs/attr[@name='deployment']/attrs/attr[@name='name']/string").get("value")
        self.saas_name = xml.find(
            "attrs/attr[@name='name']/string").get("value")
        self.account = xml.find(
            "attrs/attr[@name='account']/string").get("value")
        self.url = xml.find("attrs/attr[@name='url']/string").get("value")
        self.account_token_path = xml.find(
            "attrs/attr[@name='account_token_path']/string").get("value")

    def show_type(self):
        return "{0} [{1}]".format(self.get_type(), self.saas_name)


class saasAuthstate(nixops.resources.ResourceState):

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int)

    @classmethod
    def get_type(cls):
        return "saas-auth"

    def __init__(self, depl, name, id):
        nixops.resources.ResourceState.__init__(self, depl, name, id)
        self._conn = None
        self.token = ""

    @property
    def resource_id(self):
        return self.token

    def prefix_definition(self, attr):
        return {('resources', 'saasAuths'): attr}

    def get_definition_prefix(self):
        return "resources.saasAuths."

    def create(self, defn, check, allow_reboot, allow_recreate):
        with open(defn.account_token_path, "r") as f:
            account_token = f.readline().strip()
        headers = {'Authorization': account_token}
        r = requests.get('{}?username={}'.format(
            defn.url, defn.deployment_name), headers=headers)
        self.token = r.content
        return

    def destroy(self, wipe=False):
        return True

    def get_physical_spec(self):
        return {"token": self.token}
