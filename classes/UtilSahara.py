import time
from datetime import datetime

class UtilSahara():

    def __init__(self, connection):
        self.connection = connection

    def createDataSource(self, name, ds_url, ds_type, description="", user=None, key=None):
        print 'Creating Data Source ' + name + ' ...'
        data_source = self.connection.data_sources.create(name,
                                         description,
                                         ds_type,
                                         ds_url,
                                         user,
                                         key)
        print 'Success! Data Source has been created!'
        return data_source

    def listDataSources(self, j):
        print self.connection.data_sources.list()

    #wait time is ~ 20 min if not setted
    def deleteCluster(self, cluster_id, verify=True, wait_time=250):
        print 'Deleting cluster: ' + cluster_id
        self.connection.clusters.delete(cluster_id)

        if verify: status = self.verifyClusterDeletion(cluster_id, wait_time)
        else: 'Check succes on Horizon :)'
        return cluster_id

    #The template must exist already, wait time is ~ 20 min if not setted
	''' it creates a hadoop cluster of plugin Vanilla and version 2.6.0 ''' 
    def createClusterHadoop(self, name, image_id, template_id, net_id, user_keypair, wait_time=250, verify=True):

        print 'Creating hadoop cluster...'

        p_n = 'vanilla'
        h_v = '2.6.0'

        cluster = self.connection.clusters.create(name=name,plugin_name=p_n, hadoop_version=h_v, default_image_id = image_id, cluster_template_id=template_id, net_id=net_id, user_keypair_id=user_keypair)
        print 'Cluster is being created: ' + cluster.id

        if verify: status = self.verifyClusterCreation(cluster.id, wait_time)
        else: 'Check succes on Horizon :)'

        return cluster.id

    #wait time is equal to ~ 2 hours if not setted
    def runMapReduceJob(self, job_name, job_id, cluster_id, map_output_key, map_output_value,
        input_ds_id, output_ds_id, wait_time=1500, verify=True, map_class=None, reduce_class=None, reduces='3'):

        if map_class == None: map_class = job_name + '$Map'
        if reduce_class == None: reduce_class = job_name + '$Reduce'

        job_configs = {
            'configs' : {'mapred.mapper.class': map_class,
            'mapred.reducer.class': reduce_class,
            'mapred.reduce.tasks' : reduces,
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

        if verify:
            status = self.verifyJob(job.id, wait_time)
            return self.getJobInfo(job.id, status)
        else:
            print 'Check success on Horizon :)'

    #wait time is equal to ~ 2 hours if not setted
    def runJavaActionJob(self, main_class, job_id, cluster_id, number_maps="3", number_reduces="1", wait_time=1500, verify=True, reduces='3', input_ds_id=None, output_ds_id=None):

        job_configs = {
            'configs': {
            'mapred.reduce.tasks' : reduces,
            'edp.java.main_class' : main_class
            },
            'args': [number_maps, number_reduces]
        }

        print 'Job will be executed...'
        job = self.connection.job_executions.create(job_id,
                                        cluster_id, input_ds_id, output_ds_id,
                                        job_configs)
        print 'Job is being executed!'

        if verify:
            status = self.verifyJob(job.id, wait_time)
            return self.getJobInfo(job.id, status)
        else:
            print 'Check success on Horizon :)'

    #wait time is equal to ~ 2 hours if not setted
    def runStreamingJob(self, job_template_id, cluster_id, streaming_mapper, streaming_reducer,
        input_ds_id=None, output_ds_id=None, input_hdfs_path="", output_hdfs_path="", wait_time=1500, verify=True, reduces=1):

        job_configs = {
            'configs' : {
            'mapred.reduce.tasks' : str(reduces),
            'edp.streaming.mapper': streaming_mapper,
            'edp.streaming.reducer': streaming_reducer },
            'args': [input_hdfs_path,output_hdfs_path],
            'params': {}
        }
        
        print "job_configs:", job_configs

        job = self.connection.job_executions.create(job_template_id,
                                   cluster_id,
                                   input_ds_id,
                                   output_ds_id,
                                   job_configs)


        print 'Job is being executed: ' + job.id

        if verify:
            status = self.verifyJob(job.id, wait_time)
            return self.getJobInfo(job.id, status)
        else:
            print 'Check success on Horizon :)'

    def get_instances_ips(self, cluster_id, instance_name=None):
        instances_ip = []
        cluster = self.connection.clusters.get(cluster_id)
        print 'Getting instances IPs...'
        for node_group in cluster.node_groups:
            for instance in node_group['instances']:
                print instance['internal_ip']
                instances_ip.append(instance['internal_ip'])
                print 'Success!'
        return instances_ip

    def get_master_ip(self, cluster_id):
        cluster = self.connection.clusters.get(cluster_id)
        print 'Getting master IP...'
        for node_group in cluster.node_groups:
            for instance in node_group['instances']:
                if 'master' in instance['instance_name']:
                    master_ip = instance['internal_ip']
                    print 'master IP =', master_ip
                    return master_ip

    def get_master_id(self, cluster_id):
        cluster = self.connection.clusters.get(cluster_id)
        print 'Getting master ID...'
        for node_group in cluster.node_groups:
            for instance in node_group['instances']:
                if 'master' in instance['instance_name']:
                    master_id = instance['instance_id']
                    print 'master id =', master_id
                    return master_id

    def verifyClusterCreation(self, cluster_id, wait_time):
        cont = 0
        while True:
            time.sleep(5)
            try:
                status = self.connection.clusters.get(cluster_id).status
            except:
                print "Cluster is dead or doesn't exist!", 'id = ' + cluster_id
            print status
            if status == 'Active':
                break
            elif status == 'Error': 
                raise RuntimeError("Cluster could not be created. Check configurations or cloud status.")
            cont += 1
            if cont >= wait_time:
                print 'TIMEOUT!!!'
                break

    def verifyClusterDeletion(self, cluster_id, wait_time):
         cont = 0
         while True:
             time.sleep(5)
             try:
                 status = self.connection.clusters.get(cluster_id).status
             except:
                 print "Cluster was successfully deleted!", 'id = ' + cluster_id
                 break
             print status
             if status == 'Error':
                 raise RuntimeError("Cluster could not be created. Check configurations or cloud status.")
             cont += 1
             if cont >= wait_time:
                 print 'TIMEOUT!!!'
                 break

    def verifyJob(self, job_id, wait_time):
        cont = 0
        while True:
            time.sleep(5)
            status = self.connection.job_executions.get(job_id).info['status']
            print status
            if status in ['SUCCEEDED', 'FAILED', 'KILLED']: break
            cont += 1
            if cont >= wait_time:
                print 'TIMEOUT: job is being killed...'
                self.connection.job_executions.delete(job_id)
                break
        return status

    '''
    Returns only status, id and time of job.
    '''
    def getJobInfo(self, job_id, job_status):
        job_time = 'NOT_AVAILABLE'
        if job_status == 'SUCCEEDED':
            startTime = datetime.strptime(self.connection.job_executions.get(job_id).info['startTime'], '%a, %d %b %Y %H:%M:%S GMT')
            endTime = datetime.strptime(self.connection.job_executions.get(job_id).info['endTime'], '%a, %d %b %Y %H:%M:%S GMT')
            job_time = (endTime - startTime).total_seconds()
            print 'Time: '
            print startTime, endTime
            print 'Job id: ' + job_id
        else:
            print "Job didn't succeed so job time isn't available"
        return {'status' : job_status , 'id' : job_id, 'time' : job_time}
