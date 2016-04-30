#OpenStack Scripts

Some OpenStack scripts that may help in some habitual situations.
You can use the just the classes or the scripts as well. The scripts just show how to use the classes to do some operations more easily with the classes that use OpenStack python-client :smile:

### To use this code you should:
1. Dowload this git repository
2. Be familiar with OpenStack command-line clients - more about it [here](http://docs.openstack.org/user-guide/common/cli_overview.html).
3. Install the OpenStack command-line clients - more about it [here](http://docs.openstack.org/user-guide/common/cli_install_openstack_command_line_clients.html).
4. Set environment variables using the OpenStack RC file - more about it [here](http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html).

### The Configuration Json

To run the scripts in this folder you should have a configuration json in the same folder of your scripts with the name `configuration.json`, and set up the configurations. You can get all the configuration trough Horizon.

``` 
{
    "user" : "",
    "project_name" : "",
    "project_id" : "",
    "net_id" : "",
    "main_ip" : ""
}
```
-   user --> your username in the OpenStack cloud
-   project_name --> the project name
-   project_id --> ~~can you guess what this means?~~ You can get this through Horizon
-   net_id -> network id of the network your VM's or clusters will use
-   main_ip --> the main ip of your cloud

### Play with the code!

Now you're free to change the code and make some more scripts to do whatever you need and want :tada:
