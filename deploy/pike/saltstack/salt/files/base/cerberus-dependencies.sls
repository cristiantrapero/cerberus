pike-repository:
  pkgrepo.managed:
    - humanname: Add pike.esi.uclm.es repo
    - name: deb http://pike.esi.uclm.es/arco sid main
    - file: /etc/apt/sources.list.d/pike.list
    - key_url: http://pike.esi.uclm.es/arco/key.asc
    - refresh: True
    - reload: True

python-packages:
  pkg.installed:
    - pkgs:
      - python3
      - python-pip
      - python3-pip
    - refresh: True
    - reload: True

pike-packages:
  pkg.installed:
    - pkgs:
      - python3-zeroc-ice
      - citisim-slice
      - libcitisim
    - refresh: True
    - reload: True
    - pkgrepo: pike-repository