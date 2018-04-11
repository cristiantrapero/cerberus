pip3-dependencies:
  pip.installed:
    - pkgs:
      - watchdog
      - opencv-python
      - watchdog
      - scipy
      - numpy
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python-packages
