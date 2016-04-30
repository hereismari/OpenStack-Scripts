from ConnectionGetter import *
import time

DEF_WAITING_TIME = 2

class UtilNova():

    def __init__(self, connection):
        self.connection = connection

    #default wait time(seconds): 10 min
    def create_instance(self, name, image_name, flavor_name, network_name, wait_time=600):
	
	image = self.connection.images.find(image_name)
	flavor = self.connection.flavors.find(flavor_name)
	network = self.connection.networks.find(network_name)

	nics = [{'net-id' : network.id}]

	instance = self.connection.servers.create(name, image, flavor, network)
	
	verifyInstanceCreation(instance.id, wait_time)	        	
	return instance

    def deleteInstance(self, instance):
	print 'Deleting %s ...' % instance.networks['private-net'][0]
	self.connection.servers.delete(instance)

    def is_volume_attached(self, volume_id, server_id):
        server_volumes_ids = [v.id for v in self.connection.volumes.get_server_volumes(server_id)]
        return (volume_id in server_volumes_ids)

    def attach_volume(self, server_id, volume_id):

        print 'Attaching volume of id %s, to server of id %s' % (volume_id, server_id)
        self.connection.volumes.create_server_volume(server_id, volume_id, None)
        attached = False
        while (not attached):
            time.sleep(0.5)
            attached = self.is_volume_attached(volume_id, server_id)
        print 'Success!'

    def detache_volume(self, server_id, volume_id):

        print 'Detaching volume of id %s, to server of id %s' % (volume_id, server_id)
        self.connection.volumes.delete_server_volume(server_id, volume_id)
        attached = True
        while (attached):
            time.sleep(0.5)
            attached = self.is_volume_attached(volume_id, server_id)

        print 'Success!'

    def verifyInstanceCreation(instance_id, wait_time):

	wait_time = wait_time / 5 # status is only checked in an intervel of 5 seco:nds
	cont = 0
	while True:
	    time.sleep(5)
	    status = self.connection.server.get(instance_id).info['status']
	    print status
	    if status in ['Active', 'Error']: break
	    cont += 1
            if cont >= wait_time:
		print 'TIMEOUT: instance is being killed...'
		self.connection.server.delete(instance_id)
		break
	return status	
