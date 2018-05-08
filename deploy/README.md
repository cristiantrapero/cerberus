# Deploy of Access Control System in Smart Office

### In this tutorial we will see as to deploy the access control system based in services

To deploy the system is required different devices with a specific configurations. In this case we need the following devices:

1. **Sonoff**: To actionate the electric door opener.
2. **Raspberry Pi**: Used for run some services.
3. **Audio soundcard USB**: It is required to connect a microphone to the Raspberry Pi because it does not have a sound card.
4. **Microphone**: To record audio commands
5. **IP Camera**: To take snapshots.
6. **Server**: Used for run Icegrid Application.

This repository contains all files necesary for deploy the application in the nodes. In this case we have **two nodes**:
 - **cerberus**: In the cerberus node (located in arco.esi.uclm.es) run the icegrid app and the corresponding services.
 - **rpi**: Run an icegridnode that execute the clip and motion services.

The directory is structured as follow:
1. **pike**: Contains the cerberus Vagranfile node, the salt states and all configuration files.
2. **raspberry**: Contains the script to install the salt minion in the rpi for conect it to the cerberus node master.
3. **cerberus-test.xml**: Is an test application that executes all services in one node. Is to test that the services run correctly.


To deploy the application you need follow this steps:
1. Connect the devices properly.
2. Deploy the cerberus node with his salt master.
3. Install the salt minion in the Raspberry Pi and connect it to the salt master.
4. Run the highstate in the cerberus node for deploy the services.
