from classes.UtilSwift import *
from classes.ConnectionGetter import *
from classes.UtilSahara import *
from classes.UtilKeystone import *
import os
import sys
import subprocess
import time
import getpass

user = sys.argv[1]
key = sys.argv[2]
project_name = sys.argv[3]

project_id = 'project_id'
template_id = 'template_id' 
net_id = 'net_id'
image_id = 'image_id'

connector = ConnectionGetter(user, key, project_name, project_id, 'Openstack_IP')

keystone_util = UtilKeystone(connector.keystone())
token_ref_id = keystone_util.getTokenRef(user, key, project_name).id
sahara_util = UtilSahara(connector.sahara(token_ref_id))

sahara_util.createClusterHadoop('hadoop-create', image_id, template_id, net_id)

