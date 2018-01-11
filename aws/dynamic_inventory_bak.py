#!/usr/bin/env python

import json
import argparse


terraform_file=open('terraform.tfstate')
y=json.load(terraform_file)


parser = argparse.ArgumentParser(description='Dynamic Inventory')
parser.add_argument('--list',action = 'store_true',help='list the hosts')

def create_empty_dict(y):
   resource_dict = {}
   for i in y['modules'][0]['resources'].keys():
       if  i.split('.')[0] == "aws_instance":
           resource_dict[i.split('.')[1]]=[]
   tmp_resource_dict = resource_dict
   for i in y['modules'][0]['resources'].keys():
       if  i.split('.')[0] == "aws_instance":
           tmp_resource_dict[i.split('.')[1]].append(i)
   return tmp_resource_dict


def get_ip_address(y):
   resource_dict = {}
   tmp_resource_dict = create_empty_dict(y)
   all=[]
   for i in tmp_resource_dict.keys():
      ip_addresses=[]
      for x in tmp_resource_dict[i]:
         ip_addresses.append(y['modules'][0]['resources'][x]['primary']['attributes']['public_ip'])
      all=all+ip_addresses
      resource_dict[i]={'hosts':  ip_addresses}
      resource_dict['all'] = { 'hosts': all}
   return resource_dict

def get_host_vars(y):
    vars_dict = {}
    for i in y['modules'][0]['resources'].keys():
        if  i.split('.')[0] == "aws_instance":
           vars_dict[y['modules'][0]['resources'][i]['primary']['attributes']['public_ip']] = y['modules'][0]['resources'][i]['primary']['attributes']
    return vars_dict
    

def create_inventory(y):
    final_inventory = get_ip_address(y)
    final_inventory.update({ "_meta": { "hostvars": get_host_vars(y) }})
    return final_inventory
    
           
    
args = parser.parse_args()
if args.list:
   x=open('terraform.tfstate')
   y=json.load(x)
#   print get_host_vars(y)
#   print json.dumps(get_ip_address(y))
   print json.dumps(create_inventory(y))


