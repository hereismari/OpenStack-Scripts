from ConnectionGetter import *
import swiftclient
import os

''' Was tested is working fine! '''
class UtilSwift():

    def __init__(self, connection):
        self.connection = connection

    def storeFile(self, path, object_name, container_name):

        os.chdir(path)
        target = object_name

        print 'Transfering file ' + object_name

        with open(target, 'r') as input_file:
                self.connection.put_object(container_name, target,
                        contents = input_file.read(),
                        content_type='text/plain')

                print 'Object: ' + object_name + ' successfully transfered to '+ container_name
        
    def storeFolder(self, path, folder_name, container_name):

        os.chdir(path)
        
        print 'Transfering folder ' + folder_name
        
        for target in os.listdir(folder_name):
            object_name = folder_name + '/' + target
            self.storeFile(path, object_name, container_name)
        
        print 'Folder: ' + folder_name + ' successfully transfered to '+ container_name
        
    def getFile(self, path, object_name, container_name):

        os.chdir( path )

        print 'Getting ' + object_name + ' from ' + container_name + ' ...'
        obj = self.connection.get_object(container_name, object_name)

        print 'Saving the object in the folder...'
        with open(object_name, 'w') as object_name:
            object_name.write(obj[1])

        print 'File saved with success at:' + path
