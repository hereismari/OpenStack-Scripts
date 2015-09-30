import time

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
        print connection.data_sources.list()

    #The template must exist already, wait time ~ 20 min
    def createClusterHadoop(self, name, image_id, template_id, net_id, wait_time=250, verify=True):

        print 'Creating hadoop cluster...'

        p_n = 'vanilla'
        h_v = '2.6.0'

        cluster = self.connection.clusters.create(name=name,plugin_name=p_n, hadoop_version=h_v, default_image_id = image_id, cluster_template_id=template_id, net_id=net_id)
        print 'Cluster is being created: ' + cluster.id
        if verify: 
            cont = 0
            while True:
                time.sleep(5)
                status = self.connection.clusters.get(cluster.id).status
                print status
                if status in ['Active', 'Error']: break
                cont += 1
                if cont >= wait_time: 
                    print 'cluster is being killed...'
                    self.connection.clusters.delete(cluster)
                    break
        else: print 'check success on Horizon.'
        return cluster.id

    #wait time is equal to ~ 2 hours if not passed as a parameter
    def runMapReduceJob(self, job_name, job_id, cluster_id, map_output_key, map_output_value,
        input_ds_id, output_ds_id, wait_time=1500, verify=True):

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

        print 'Job is being executed: ' + job.id
        if verify:
            cont = 0
            while True:
                time.sleep(5)
                status = self.connection.job_executions.get(job.id).info['status']
                print status
                if status in ['SUCCEEDED', 'FAILED', 'KILLED']: break
                cont += 1
                if cont >= wait_time: 
                    print 'job is being killed...'
                    self.connection.job_executions.delete(job)
                    break
        else: print 'check success on Horizon'
        return job.id

    #wait time is equal to ~ 2 hours if not passed as a parameter
    def runJavaActionJob(self, job_name, job_id, cluster_id, number_maps, number_reduces, wait_time=1500, verify=True):

        job_configs = {
            'configs': {
                    'edp.java.main_class' : job_name
                },
            'args': [number_maps, number_reduces]
        }

        print 'Job wiil be executed...'
        job = self.connection.job_executions.create(job_id,
                                        cluster_id, None, None,
                                        job_configs)
        print 'Job is being executed!'
        if verify:
            cont = 0
            while True:
                time.sleep(5)
                status = self.connection.job_executions.get(job.id).info['status']
                print status
                if status in ['SUCCEEDED', 'FAILED', 'KILLED']: break
                cont += 1
                if cont >= wait_time: 
                    print 'job is being killed...'
                    self.connection.job_executions.delete(job)
                    break
        else: print 'check success on Horizon'
        return job.id
