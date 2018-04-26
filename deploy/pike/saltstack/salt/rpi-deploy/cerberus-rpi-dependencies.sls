motion-sensor-dependencies:
  pip.installed:
    - pkgs:
      - watchdog
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules

clip-service-dependencies:
  pip.installed:
    - pkgs:
      - scipy
      - numpy
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules

snapshot-service-dependencies:
  pip.installed:
    - pkgs:
      - opencv-python
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules
      - pkg: opencv-dependencies

authenticator-service-dependencies:
  pip.installed:
    - pkgs:
      - apiai
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules
