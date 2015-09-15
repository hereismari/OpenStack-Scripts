import swiftclient
import subprocess
import os

class UtilSahara():

    def __init__(self, connection):
        self.connection = connection

    def createDataSource(self, name, container, container_url, user, key):

        print 'Creating Data Source ' + name + ' ...'
        data_source = self.connection.data_sources.create(name,
                                         container,
                                         'swift',
                                         container_url,
                                         user,
                                         key)

        print 'Success! Data Source has been created!'
        return data_source

    def listDataSources(self):
        print self.connection.data_sources.list()

    def runMapReduceJob(self, job_name, job_id, cluster_id, map_output_key, map_output_value,
        input_ds_id, output_ds_id):

        job_configs = {
            'configs' : {'mapred.mapper.class': job_name + '$Map',
            'mapred.reducer.class': job_name + '$Reduce',
            'mapred.mapoutput.key.class': 'org.apache.hadoop.io.' + map_output_key,
            'mapred.mapoutput.value.class': 'org.apache.hadoop.io.' + map_output_value},
            'args': [],
            'params': {}}

        print 'Job will be executed...'
        job = self.connection.job_executions.create(job_id,
                                   cluster_id,
                                   input_ds_id,
                                   output_ds_id,
                                   job_configs)

        print 'Finished Job - check success on Horizon'
