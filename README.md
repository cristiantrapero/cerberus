## Plugable services repository, Icegrid applications and Scone knowledge.

The repository is structured as follows:

 - **config**: Icegrid application and configuration files for dummy app.
 - **deploy**: Icegrid applications for test and deploy the system. The config files has been migrated to arco.provision repository.
 - **devices**: Embedded services in devices with its corresponding PlatformIO projects.
 - **doc**: Invocation diagrams for the services and scheduler.
 - **install-dependencies.sh**: Bash script to install the services dependencies.
 - **Makefile**: To run cerberus dummy application.
 - **scheduler**: Scheduler for setObservers between services
 - **scone-knowledge.d**: Scone knowledge for the plugable services.
 - **services**: Plugable services.
 - **tests**: Unitary tests for Scone knowledge.
 - **utils**: Util services.


 **How to run the system**: http://pike.esi.uclm.es:8012/recipe/how_to_run_cerberus_icegrid_application/
 
|      Services         | dummy | real | debian package | Dockerfile |
|:---------------------:|:-----:|:----:|:--------------:|:----------:|
| **motion-sensor**     |  yes  |  yes |       yes      |      no    |
| **snapshot-service**  |  yes  |  yes |       yes      |      no    |
| **clip-service**      |  yes  |  yes |       yes      |      no    |
| **person-recognizer** |  yes  |  yes |       yes      |      no    |
| **speech-to-text**    |  yes  |  yes |       yes      |      no    |
| **authenticator**     |  yes  |  yes |       yes      |      no    |
| **door-actuator**     |  yes  |  yes |  not available |      no    |
| **scheduler**         |  yes  |  no  |       no       |      no    |
| **simulate-motion**   |  yes  |  no  |       no       |      no    |

**To execute the real services it is necessary to have access tokens to the IBM speech to text and Dialogflow APIs.**

There are some default credentials created by Cristian:

#### Speech to text:
 - SpeechToText.APIKey = **YajA1aReGIFhE0GtZMdhPmysvcm82DrI901L5FOM0Jp7**
 - SpeechToText.URL = **https://gateway-lon.watsonplatform.net/speech-to-text/api**

#### Authenticator:
 - Authenticator.DialogflowToken = **aedd62ed20ba4697b39d214b7d727c16**