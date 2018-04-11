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
      - property-service-simple
      - citisim-wiring-service
    - refresh: True
    - reload: True
    - pkgrepo: pike-repository

pip3-dependencies:
  pip.installed:
    - pkgs:
      - watson-developer-cloud
      - service-identity
      - dlib
      - numpy >= 1.1, < 2.0
      - scipy >= 0.13, < 0.17
      - pandas >= 0.13, < 0.18
      - scikit-learn >= 0.17, < 0.18
      - nose >= 1.3.1, < 1.4
      - nolearn == 0.5b1
      - opencv-python
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python-packages

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
