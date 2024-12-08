Role Name
=========

fail2ban

Requirements
------------

This role has no pre-requisites.

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
         - fail2ban
