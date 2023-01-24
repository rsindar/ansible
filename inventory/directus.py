#!/usr/bin/env python3

import os
import sys
import argparse
import json
import requests
from requests.exceptions import HTTPError
import urllib3

inventory = {'_meta': {'hostvars': {}}, 'all': {'children': ['ungrouped']}, 'ungrouped': {'hosts': []}}
cmdb_url = 'https://directus.tld.local/items/host?fields=hostname&fields=network_interface&fields=operating_system&fields=ansible_groups&fields=environment&fields=location&limit=-1&filter=%7B%22state%22%3A%22online%22%7D'


def set_cmdb_headers():
    if not os.environ.get('CMDB_TOKEN'):
        print('ERROR! The required "CMDB_TOKEN" environment variable is not defined')
        sys.exit(1)
    return {'Authorization': 'Bearer ' + os.environ['CMDB_TOKEN']}


def add_host_to_group(group, host):
    try:
        inventory['all']['children'].index(group)
    except ValueError:
        inventory['all']['children'].append(group)
        inventory.update({group: {'hosts': []}})
    inventory[group]['hosts'].append(host)


def extract_ip_address(network_interfaces):
    try:
        interface_info = network_interfaces[0]
    except IndexError:
        interface_info = network_interfaces
    return interface_info.split(':')[1].lstrip().split(' ', 1)[0]


def fulfill_inventory():
    try:
        urllib3.disable_warnings()
        response = requests.get(cmdb_url, headers=set_cmdb_headers())
        response.raise_for_status()
        json_response = response.json()
        hosts_list = json_response['data']
        for host in hosts_list:
            if host['hostname'] and host['network_interface'] and host['network_interface']:
                host['hostname'] = host['hostname'].lower()
                inventory['_meta']['hostvars'].update({host['hostname']: {'ansible_host': extract_ip_address(host['network_interface'])}})
                if not host['ansible_groups'] and not host['environment'] and (not host['location'] or host['location'] == 'UNKNOWN'):
                    inventory['ungrouped']['hosts'].append(host['hostname'])
                else:
                    if host['location'] and host['location'] != 'UNKNOWN':
                        add_host_to_group(host['location'].lower() + '_loc', host['hostname'])
                    if host['environment'] and host['environment'] != 'UNKNOWN':
                        add_host_to_group(host['environment'].lower() + '_env', host['hostname'])
                    if host['ansible_groups']:
                        for group in host['ansible_groups']:
                            add_host_to_group(group, host['hostname'])
                    if str(host['operating_system']).find('Microsoft') >= 0:
                        add_host_to_group('windows', host['hostname'])
                    if str(host['operating_system']).find('CentOS') >= 0 \
                            or str(host['operating_system']).find('Red Hat') >= 0 \
                            or str(host['operating_system']).find('Ubuntu') >= 0:
                        add_host_to_group('linux', host['hostname'])
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')


def parse_args():
    parser = argparse.ArgumentParser(description='Directus CMDB inventory script')
    arguments_group = parser.add_mutually_exclusive_group(required=True)
    arguments_group.add_argument('--list', action='store_true')
    arguments_group.add_argument('--host')
    arguments_group.add_argument('--group')
    return parser.parse_args()


def main():
    args = parse_args()
    fulfill_inventory()
    if args.list:
        print(json.dumps(inventory, indent=4))
    if args.host:
        try:
            print(json.dumps(inventory['_meta']['hostvars'][args.host], indent=4))
        except KeyError:
            print('ERROR! You must pass a single valid host to --host parameter')
    if args.group:
        try:
            print(json.dumps(inventory[args.group], indent=4))
        except KeyError:
            print('ERROR! You must pass a single valid group to --group parameter')


if __name__ == '__main__':
    main()
