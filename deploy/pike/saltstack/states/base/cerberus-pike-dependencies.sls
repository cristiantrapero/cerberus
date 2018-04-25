pike-services-for-cerberus:
  pkg.installed:
    - pkgs:
      - zeroc-ice36
      - scone
      - scone-wrapper
      - dharma
      - property-service-simple
      - citisim-wiring-service
    - refresh: True
    - reload: True
    - pkgrepo: pike-repository

person-recognizer-dependencies:
  pip.installed:
    - pkgs:
      - numpy >= 1.1, < 2.0
      - scipy >= 0.13, < 0.17
      - pandas >= 0.13, < 0.18
      - scikit-learn >= 0.17, < 0.18
      - nose >= 1.3.1, < 1.4
      - nolearn == 0.5b1
      - opencv-python
      - dlib
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules

torch-repository:
  git.latest:
    - name: https://github.com/torch/distro.git
    - target: ~/torch
    - force_checkout: True

install-torch:
  cmd.run:
    - name: bash install-deps; ./install.sh; source ~/.bashrc
    - cwd: ~/torch
    - require:
      - git: torch-repository

install-torch-dependencies:
  cmd.run:
    - name: for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done
    - require:
      - pkg: install-torch

openface-repository:
  git.latest:
    - name: https://github.com/cmusatyalab/openface.git
    - target: /tmp/openface
    - force_checkout: True

install-openface-python-module:
  cmd.run:
    - name: python3 setup.py install
    - cwd: /tmp/openface/
    - require:
      - pkg: python-packages
      - git: openface-repository

speech-to-text-dependencies:
  pip.installed:
    - pkgs:
      - watson-developer-cloud
      - service-identity
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-packages
      - pkg: citisim-modules
