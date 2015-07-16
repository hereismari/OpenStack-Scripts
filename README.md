# Upload-object-inside-openstack-swift
Basic Scripts and tutorial for upload a object inside openstack swift(Using Ubuntu Linux).
In this tutorial it's supposed you have access to an openstack distribution and a project in it.

# What do I need in order to be able to upload a file through linux terminal?

1. you need a openrc.sh file of your project, you can get one with the following steps:

      1.1 Go to openstack horizon, you'll have a menu with the option Compute -> Access & Security
      
      1.2 In Access & Security there is a view option called API access
      
      1.3 In API Access there is a button "Download Openstack RC file", click on it.
      
      1.4 Done!

2. Execute these commands at bash:

      2.1 $ sudo apt get install python-dev

      2.2 $ sudo apt get install python-pip

      2.3 $ sudo pip install python-swiftclient

      2.4 $ sudo pip install python-keystoneclient

3. Launch the openrc-sh script:

      3.1 $ source your_project-openrc.sh

      Obs: you can edit OS_PASSWORD="your password", so it don't asks your password anymore.

4. You're ready to upload files to swift openstack!

