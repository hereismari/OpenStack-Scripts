from ConnectionGetter import *
import time

DEF_WAITING_TIME = 2

class UtilNova():

    def __init__(self, connection):
        self.connection = connection

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


