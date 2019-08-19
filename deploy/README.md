# Deploy of Access Control System in Smart Office

### In this tutorial we will see as to deploy the access control system based in services

To deploy the system is required different devices with a specific configurations. In this case we need the following devices:

1. **Sonoff**: To actionate the electric door opener.
2. **Raspberry Pi**: Used to run some services.
3. **Audio soundcard USB**: It is required to connect a microphone to the Raspberry Pi because it does not have a sound card.
4. **Microphone**: To record audio commands.
5. **IP Camera**: To take snapshots.
6. **Server**: Used for run Icegrid Application.

This repository contains all files necesary for deploy the application in the nodes. In this case we have **two nodes**:
 - **cerberus**: In the cerberus node (located in pike.esi.uclm.es) run the icegrid app and the corresponding services.
 - **cerverus-rpi**: Run an icegridnode that execute the clip and motion services.

The directory is structured as follow:
1. **cerberus-app.xml**: This is the application that executes the real system in the two Icegrid nodes.
2. **cerberus-test-app.xml**: Is an test application that executes all services in one node. Is to test that the services run correctly.


To deploy the system you need follow this steps:
1. Connect the devices and hardware properly.
2. Install Raspbian and Salt minion in the Raspberry Pi. Connect the cerberus-rpi minion to the syndic Salt server.
3. Deploy the Vagrant node for cerberus in pike server. https://bitbucket.org/arco_group/arco.provision/src/default/pike/Vagrantfile
4. Provision the Salt minions running the highstate in the syndic node.
5. Add cerberus-app.xml to the cerberus Icegrid registry to run the system.
6. Run the scheduler to connect the services.
7. Run the command: make connect-authenticator-to-sonoff. to connect the authenticator service to the sonoff. Check the IP of the Sonoff first.
8. Check that everything is working fine.
