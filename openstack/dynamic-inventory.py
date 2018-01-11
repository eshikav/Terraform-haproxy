#!/usr/bin/env python
try:
   import json
except ImportError:
   print "json module is needed for the dynamic inventory to work"
   exit(10)
try:   
   import re
except ImportError:
   print "re,regular expression module is needed for the dynamic inventory to work"
   exit(10)
try:
   import argparse
except ImportError:
   print "argparse expression module is needed for the dynamic inventory to work"
   exit(10)


parser = argparse.ArgumentParser(description='Dynamic Inventory')
parser.add_argument('--list',action = 'store_true',help='list the hosts')

hostVars = {"_meta": {"hostvars": {}}}
allHosts = {"all": {"hosts": []}}
floatingIpMappings = {}
groups = {}

#get the floating ips of the instances,this will reurn a hash of fixedips and its corresponding floatingip's
def getFloatingIps(config):
  reObj = re.compile('openstack_compute_floatingip_associate_v2.*')
  for key in config['modules'][0]['resources']:
      if (reObj.match(key)):
          fixedIp = config['modules'][0]['resources'][key]['primary']['attributes']['fixed_ip']
          floatingIp = config['modules'][0]['resources'][key]['primary']['attributes']['floating_ip']
          floatingIpMappings[fixedIp] = floatingIp
  return floatingIpMappings

#Create the Dynamic inventory from the terraform.tfstate file produced from the terrafom,
def createInventory(config):
    reObj = re.compile('openstack_compute_instance_v2.*')
    for key in config['modules'][0]['resources']:
       if (reObj.match(key)):
          groupName = config['modules'][0]['resources'][key]['primary']['attributes']['name'].split('-')[0]
          fixedIp = config['modules'][0]['resources'][key]['primary']['attributes']['network.0.fixed_ip_v4']
          nodeAttributes = config['modules'][0]['resources'][key]['primary']['attributes']
          if groupName  not in groups.keys():
             groups[groupName] = {'hosts' : []}
             floatingIpMappings = getFloatingIps(config)
             if fixedIp in floatingIpMappings.keys():
                  groups[groupName]['hosts'].append(floatingIpMappings[fixedIp])
                  allHosts['all']['hosts'].append(floatingIpMappings[fixedIp])
             else:
                 groups[groupName]['hosts'].append(fixedIp)
                 allHosts['all']['hosts'].append(fixedIp)
          else:
             groups[groupName]['hosts'].append(fixedIp)
             allHosts['all']['hosts'].append(fixedIp)
          hostVars["_meta"]['hostvars'][fixedIp] = config['modules'][0]['resources'][key]['primary']['attributes']
          floatingIpMappings = getFloatingIps(config)
          if fixedIp in floatingIpMappings.keys():
              hostVars["_meta"]['hostvars'][fixedIp]['floatingip'] = floatingIpMappings[fixedIp]
    groups.update(hostVars)
    groups.update(allHosts)
    return groups
    
args = parser.parse_args()
if args.list:
   try:
      terraformFile  = open('terraform.tfstate')
      terraformState = json.load(terraformFile)
      print json.dumps(createInventory(terraformState))
   except IOError:
      print "unable to find the terraform.tfstate in the current location"
      exit(11)

