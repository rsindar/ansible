Description
-----------

Deploy prometheus node exporter using ansible.

NB! Please review the original role before using this one - https://prometheus-community.github.io/ansible/

Requirements
------------

This role has no pre-requisites.

Role Variables
--------------

This role has two settable variables:
- node_exporter_version
- node_exporter_url

Dependencies
------------

This role has no dependencies.

Example Playbook
----------------

    - hosts: servers
      become: true
      roles:
         - node_exporter
