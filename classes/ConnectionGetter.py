import swiftclient
from novaclient.v2 import client as novaclient
from keystoneclient.v2_0 import client as keystoneclient
from saharaclient.api.client import Client as saharaclient
import sys
import os
import subprocess

class ConnectionGetter(object):

    def __init__(self, user, key, project_name, project_id, main_ip):
        self.user = user
        self.key = key
        self.project_name = project_name
        self.project_id = project_id
        self.main_ip = main_ip

    ''' Was tested is working fine! '''
    def sahara(self, token_id):

        print 'Establishing connection to Sahara...'

        sahara_url = 'http://%s:8386/v1.1/%s' % (self.main_ip, self.project_id)
        sahara_client = saharaclient(sahara_url=sahara_url, input_auth_token=token_id)

        print 'Connected to Sahara'
        return sahara_client

    ''' Was tested is working fine! '''
    def keystone(self):

        print 'Establishing connection to Keystone...'

        keystone_connection = keystoneclient.Client(username=self.user,
                                 password=self.key,
                                 tenant_name=self.project_name,
                                 auth_url = 'http://%s:5000/v2.0' % self.main_ip)

        print 'Connected to Keystone'
        return keystone_connection

    ''' Was tested is working fine! '''
    def swift(self):

        osOptions = dict()
        osOptions['user_domain_name'] = 'user_domain_name'
        osOptions['project_domain_name'] = 'project_domain_name'
        osOptions['project_name'] = self.project_name

        print 'Establishing connection to Swift...'

        swift_connection = swiftclient.Connection(
                user=self.user,
                key=self.key,
                authurl='http://%s:5000/v3' % self.main_ip,
                os_options=osOptions,
                auth_version=3,
        )

        print 'Connected to Swift'
        return swift_connection

