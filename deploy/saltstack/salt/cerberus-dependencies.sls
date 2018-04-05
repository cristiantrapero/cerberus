pike-repo:
  pkgrepo.managed:
    - humanname: Add pike.esi.uclm.es repo
    - name: deb http://pike.esi.uclm.es/arco sid main
    - file: /etc/apt/sources.list.d/pike.list
    - key_url: http://pike.esi.uclm.es/arco/key.asc

python3:
  pkg.installed

python3-pip:
  pkg.installed

cmake:
  pkg.installed

git:
  pkg.installed

python3-zeroc-ice:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

zeroc-ice36:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

scone:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

scone-server:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

scone-wrapper:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

dharma:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

citisim-slice:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

libcitisim:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

citisim-wiring-service:
  pkg.installed:
  - require:
    - pkgrepo: pike-repo

opencv-python:
  pip.installed:
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-pip

watson-developer-cloud:
  pip.installed:
    - name: watson-developer-cloud
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-pip

whatchdog:
  pip.installed:
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-pip

service-identity:
  pip.installed:
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-pip

dlib:
  pip.installed:
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python3-pip

openface:
  git.latest:
    - name: https://github.com/cmusatyalab/openface.git
    - target: /tmp/openface
    - force_checkout: True
    - require:
      - pkg: git


install-openface:
  cmd.run:
    - name: pip3 install -r /tmp/openface/requeriments.txt
    - require:
      - pkg: python3-pip
      - git: openface
