from classes.UtilSwift import *
from classes.ConnectionGetter import *
from classes.UtilSahara import *
from classes.UtilKeystone import *
from utils.JsonParser import *

import os
import sys
import subprocess
import time
import getpass

def howToUse():
    how_to_use = '$python runStreamingJob.py <job> <file_name> <cluster_id>'
    print 'How to use:'
    print how_to_use

password = getpass.getpass('password: ')

parser = JsonParser('configuration2.json')
user = parser.get('user')
project_name = parser.get('project_name')
project_id = parser.get('project_id')
main_ip = parser.get('main_ip')

streaming_mapper = '/bin/cat'
streaming_reducer = '/usr/bin/wc - l'
input_hdfs_path = 'input'
output_hdfs_path = 'output-test'

job_id = 'f915cb23-9ab2-4476-8323-6b8381fd69d0'
cluster_id = '01b4a929-2ab2-43e6-8b3a-c6e163fe6f72'

exec_date = time.strftime('%Y%m%d%H%M%S')

connector = ConnectionGetter(user, password, project_name, project_id, main_ip)

keystone_util = UtilKeystone(connector.keystone())
token_ref_id = keystone_util.getTokenRef(user, password, project_name).id
sahara_util = UtilSahara(connector.sahara(token_ref_id))

input_ds_name = 'input_' + exec_date
input_ds_url = "/user/hadoop/" + input_hdfs_path
input_ds_id = sahara_util.createDataSource(input_ds_name, input_ds_url, 'hdfs', user, password)

output_ds_name = 'output_' + exec_date
output_ds_url = "/user/hadoop/" + output_hdfs_path
output_ds_id = sahara_util.createDataSource(output_ds_name, output_ds_url, 'hdfs', user, password)

sahara_util.runStreamingJob(job_id, cluster_id, streaming_mapper = streaming_mapper, streaming_reducer = streaming_reducer, input_ds_id = input_ds_id, output_ds_id = output_ds_id)
