### Plugable services repository, Icegrid applications and Scone knowledge.

The repository is structured as follows:

 - **services**: Plugable services.
 - **devices**: Embedded services in devices with its corresponding PlatformIO projects.
 - **scone-knowledge.d**: Scone knowledge for the plugable services.
 - **config**: Icegrid applications and config files.
 - **test**: Unitary tests for Scone knowledge.
 - **install-dependencies.sh**: Bash script to install the services dependencies.


|      Services     | dummy | real | debian package |
|:-----------------:|:-----:|:----:|:--------------:|
| motion-sensor     |  yes  |  yes |       yes      |
| snapshot-service  |  yes  |  yes |       yes      |
| clip-service      |  yes  |  yes |       yes      |
| person-recognizer |  yes  |  yes |       no       |
| speech-to_text    |  yes  |  yes |       yes      |
| authenticator     |  yes  |  yes |       yes      |
| door-actuator     |  yes  |  yes |       -        |
| scheduler         |  yes  |  no  |       no       |
| simulate_motion   |  yes  |  no  |       no       |
