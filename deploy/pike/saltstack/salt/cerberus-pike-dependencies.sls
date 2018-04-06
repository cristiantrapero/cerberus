debian-packages:
  pkg.installed:
    - pkgs:
      - cmake
      - git
    - refresh: True
    - reload: True

arco-packages:
  pkg.installed:
    - pkgs:
      - zeroc-ice36
      - scone
      - scone-wrapper
      - dharma
      - citisim-wiring-service
    - refresh: True
    - reload: True
    - pkgrepo: pike-repo

pip3-dependencies:
  pip.installed:
    - pkgs:
      - opencv-python
      - watson-developer-cloud
      - watchdog
      - service-identity
      - dlib
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python-packages

openface-repository:
  git.latest:
    - name: https://github.com/cmusatyalab/openface.git
    - target: /tmp/openface
    - force_checkout: True

install-openface-pip-dependencies:
  cmd.run:
    - name: pip3 install -r /tmp/openface/requirements.txt
    - require:
      - pkg: python-packages
      - git: openface-repository

install-openface:
  cmd.run:
    - name: python3 setup.py install
    - require:
      - pkg: python-packages
      - git: openface-repository
