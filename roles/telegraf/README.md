Description
-----------

Deploy telegraf using ansible.

NB! Please review the original guide before using this role - https://docs.influxdata.com/telegraf/v1/install/

Requirements
------------

Red Hat Linux distribution.

Role Variables
--------------

This role has no settable variables.

Dependencies
------------

This role has no dependencies.

Example Playbook
----------------

    - hosts: servers
      become: true
      roles:
         - telegraf
