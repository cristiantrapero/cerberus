pike-repository:
  pkgrepo.managed:
    - humanname: Add pike.esi.uclm.es repo
    - name: deb http://pike.esi.uclm.es/arco sid main
    - file: /etc/apt/sources.list.d/pike.list
    - key_url: http://pike.esi.uclm.es/arco/key.asc
    - refresh: True
    - reload: True

python3-packages:
  pkg.installed:
    - pkgs:
      - python3
      - python3-pip
      - python-pip
    - refresh: True
    - reload: True

citisim-modules:
  pkg.installed:
    - pkgs:
      - python3-zeroc-ice
      - citisim-slice
      - libcitisim
    - refresh: True
    - reload: True
    - pkgrepo: pike-repository

opencv-dependencies:
  pkg.installed:
    - pkgs:
      - build-essential
      - cmake
      - git
      - libgtk2.0-dev
      - pkg-config
      - libavcodec-dev
      - libavformat-dev
      - libswscale-dev
