## Plugable services repository, Icegrid applications and Scone knowledge.

The repository is structured as follows:

 - **config**: Icegrid applications and configuration files for dummy app.
 - **deploy**: Icegrid applications for test and deploy system. The config files has been migrated to arco.provision repository.
 - **devices**: Embedded services in devices with its corresponding PlatformIO projects.
 - **doc**: Invocation diagrams for the services and scheduler.
 - **install-dependencies.sh**: Bash script to install the services dependencies.
 - **Makefile**: To run cerberus dummy application.
 - **scheduler**: Scheduler for setObservers between services
 - **scone-knowledge.d**: Scone knowledge for the plugable services.
 - **services**: Plugable services.
 - **tests**: Unitary tests for Scone knowledge.
 - **utils**: Util services.
 
|      Services     | dummy | real | debian package |
|:-----------------:|:-----:|:----:|:--------------:|
| motion-sensor     |  yes  |  yes |       yes      |
| snapshot-service  |  yes  |  yes |       yes      |
| clip-service      |  yes  |  yes |       yes      |
| person-recognizer |  yes  |  yes |       yes      |
| speech-to_text    |  yes  |  yes |       yes      |
| authenticator     |  yes  |  yes |       yes      |
| door-actuator     |  yes  |  yes |  not available |
| scheduler         |  yes  |  no  |       no       |
| simulate_motion   |  yes  |  no  |       no       |

**To execute the real services it is necessary to have access tokens to the IBM speech to text and Dialogflow APIs.**
There are some default credentials created by Cristian:

#### Speech to text:
 - SpeechToText.IBMusername = **beddfe97-4bb8-4745-a19a-32e439e04577**
 - SpeechToText.IBMpassword = **0OqAwO8uYIjV**

#### Authenticator:
 - Authenticator.DialogflowToken = **aedd62ed20ba4697b39d214b7d727c16**