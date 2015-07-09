# -*- coding: utf-8 -*- 

###########################################################################
## Chris @ DCSLAB, NCTU
## get_nodes.py
## Get the node and load balancer list
###########################################################################

from optparse import OptionParser
import xml.etree.ElementTree as ET

from libcloud.compute.types import Provider as LibCloudComputeProvider
from libcloud.loadbalancer.types import Provider as LibCloudLBProvider
from libcloud.compute.providers import get_driver as get_driver_provider
from libcloud.loadbalancer.providers import get_driver as get_driver_loadbalancer
#from libcloud.compute.providers import DRIVERS
#from libcloud.compute.base import Node

import myheader as chris


def get_nodes(key_file, providers):
	
	#----- get drivers -----
	drivers_provider = []
	drivers_loadbalancer = []

	for provider in providers:
		try:
			d = get_driver_provider(getattr(LibCloudComputeProvider, provider.name))
		except Exception, err:
			print('Error: Getting driver failed ' + provider.name + ' : ' + str(err))
			exit()
		print('debug: get_driver() of nodes: ')
#		print(d)
		driver = d(provider.id, provider.key, region = provider.region)
		# Keep in mind that some drivers take additional arguments such as region and api_version
#	print('node driver:')
#	members = [attr for attr in dir(driver) if not callable(attr) and not attr.startswith("__")]
#	i = 1
#	for member in members:
#		print('\t(' + str(i) + '): ' + member+': '+str(getattr(driver, member)))
#		i = i + 1
		drivers_provider.append(driver)

		try:
			d = get_driver_loadbalancer(getattr(LibCloudLBProvider, provider.lb))
		except Exception, err:
			print('Error: Getting driver failed ' + provider.lb + ' : ' + str(err))
			exit()
		print('debug: get_driver() of loadbalancer: ')
#		print(d)
		driver = d(provider.id, provider.key, provider.region)
#	print('lb driver:')
#	i = 1
#	members = [attr for attr in dir(driver) if not callable(attr) and not attr.startswith("__")]
#	for member in members:
#		print('\t(' + str(i) + '): ' + member+': '+str(getattr(driver, member)))
#		i = i+1
		drivers_loadbalancer.append(driver)


	#----- get node list -----
	statemap = chris.StateMap()

	def getnode(drivers_provider):
		allnode = []
		allimage = []
		for driver in drivers_provider:
			nodes = driver.list_nodes()
#			print('debug: nodes of driver ' + driver.name + ' = ' + str(len(nodes)) + ': ')
#			c = 1
#			for node in nodes:
#				print('\t' + str(c) + ': ' + str(node.name) + '  id=' + node.id + '  type=' + node.extra['instance_type'] + '  status=' + node.extra['status'])
#				c = c + 1
#			members = [attr for attr in dir(node) if not callable(attr) and not attr.startswith("__")]
#			i = 1
#			for member in members:
#				print('\t('+str(i)+'). '+member+': '+str(getattr(node, member)))
#				i=i+1
			images = driver.list_images(ex_owner='self')
			allnode.extend(nodes)
			allimage.extend(images)
		print('debug: allnode= ' + str(len(allnode)))
		print('debug: allimage= ' + str(len(allimage)))
		return (allnode, allimage)

	def getlb(drivers_loadbalancer):
		alllb = []
		for driver in drivers_loadbalancer:
			balancers = driver.list_balancers()
#		print('debug: balancers= ' + str(len(balancers)) + ': ')
			#c = 1
			#for lb in balancers:
			#	print(str(c) + ': ' + str(lb.id) + '  status= ' + str(lb.state))
			#	ms = lb.list_members()
			#	for m in ms:
			#		print('\t' + str(m))
			#	c = c + 1
#			members = [attr for attr in dir(lb) if not callable(attr) and not attr.startswith("__")]
#			i = 1
#			for member in members:
#				print('\t(' + str(i) + '). ' + member + ': ' + str(getattr(lb, member)))
#				i = i + 1
			alllb.extend(balancers)
		print('debug: allbalancer= ' + str(len(alllb)))
		return alllb

	allnode, allimage = getnode(drivers_provider)
	alllb = getlb(drivers_loadbalancer)
	
	return (allnode, alllb, allimage)