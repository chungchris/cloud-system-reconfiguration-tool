# -*- coding: utf-8 -*- 

###########################################################################
## Chris @ DCSLAB, NCTU
## get_nodes.py
## Modify the system data structure with the reconfig command
## and generate a temp config file finally
###########################################################################

import myheader as chris


def reconfig_single(options, system, allnode, alllb, modifyxml = True):
	#----- Adjust the temp congif file if in ConfigSingle mode ----- 
	# check the cluster name
	print('debug: system name: ' + str(system.name))
	find_cluster = False 
	for cluster in system.clusters:
		if cluster.name == options.target_cluster:
			find_cluster = True
			# check the scale type
			if cluster.scaletype == 'UP':
				if options.scale_type == 'out':
					print('Error: -t should only be \'up\' because the cluster ' + str(cluster.name) + ' is a scale-up cluster')
					print('All changes discarded')
					return False
				else:
					if not cluster.resize(options.scale_direct, options.scale_policy):
						print('Error: Resize failed')
						print('All changes discarded')
						return False
			elif cluster.scaletype == 'OUT':
				# scale up	
				if options.scale_type == 'up':
					if not cluster.resize(options.scale_direct, options.scale_policy):
						print('Error: Resize failed')
						print('All changes discarded')
						return False
				# scale out
				else:
					if options.scale_direct == 'a':
						if cluster.running_max != None and ((cluster.running + 1) > cluster.running_max):
							print('Meet the max running node limit')
							print('All changes discarded')
							return False
						else:
							cluster.running = cluster.running + 1
							print('Add node in the cluster ' + cluster.name)
					elif options.scale_direct == 'd':
						if not (cluster.running - 1) < 0:
							cluster.running = cluster.running - 1
							print('Decrease node in the cluster ' + cluster.name)
						else:
							print('Already no running node in this cluster')
							print('All changes discarded')
							return False
			break
	if not find_cluster:
		print('Error: No cluster named ' + options.target_cluster)
		print('All changes discarded')
		return False
			
	if modifyxml:
		system.generate_xml('configuration.tmp.xml')
	else:
		system.generate_xml('configuration.preview.xml')
	print('debug: temp config file generated')
	
	return True