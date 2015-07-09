from optparse import OptionParser
import xml.etree.ElementTree as ET
import os.path

import myheader as chris
import get_keys
import get_nodes
import reconfig_single
import gui_key
import gui_cluster
import gui_reconfigsingle


#----- input check -----
parser = OptionParser()

parser.add_option('-m', '--mode', 		dest = 'mode', 			default = None, 		help = "\"u\" for update the system state; \"b\" for beginning mode; \"rs\" for reconfig single cluster; \"rx\" for reconfig with xml file") # necessary

parser.add_option('-k', '--key', 		dest = 'key_file', 		default = "KEY.xml", 	help = "Default is \"KEY.xml\". Edit the \"KEY.xml\" in advance to provide necessary keys for accessing cloud resource")
parser.add_option('-s', '--config', 	dest = 'config_file', 	default = "reconfiguration.xml", help = "Default is \"reconfiguration.xml\". The file claims the configuration")

parser.add_option('-c', '--cluster', 	dest = 'target_cluster', default = None, 		help = "Which cluster to be scaled")
parser.add_option('-t', '--type', 		dest = 'scale_type', 	default = None, 		help = "\"up\" for scaling up the cluster; \"out\" for scaling out the cluster")
parser.add_option('-d', '--direct', 	dest = 'scale_direct', 	default = None, 		help = "\"a\" for adding resource; \"d\" for decreasing resource")
parser.add_option('-o', '--handoff', 	dest = 'handoff', 	default = 'n', 		help = "y/n. Use specified img file as lunching new instance")
#parser.add_option('-l', '--level', dest='scale_level', default=None, help="add/decrease the cluster in what degree(level)")
parser.add_option('-p', '--policy', 	dest = 'scale_policy', 	default = 'ram', 		help = "Scale policy: \"vcpu\", \"ram\", \"disk\", \"bandwidth\", \"price\". Default is ram")

parser.add_option('-i', '--iniscript', 	dest = 'active_ini_script', default = 'y', 		help = "y/n. Activate the initialization script or not. Default is yes")

parser.add_option('-f', '--straightforward', dest = 'straightforward', default = 'n', 	help = "y/n. Straightforwardly go through the confirming steps, i.e. no waiting, no confirming. Default is not")
parser.add_option('-g', '--gui', 		dest = 'gui', 			default = 'y', 			help = "y/n. Enable the GUI or not. Default is yes")
#parser.add_option('-a', '--automation', dest = 'auto', 			default = 'n', 			help = "y/n. Give \"y\" if you use this tool for some kind of automatically iterative procedure. Default is not")

(options, args) = parser.parse_args()
#if options.gui == 'n' and options.mode == None:
#	print('If not using GUI, -m option should be \"u\" for update mode; \"b\" for beginning mode; \"rs\" for reconfig single cluster; \"rx\" for reconfig with xml file')
#	exit()
if options.mode == 'rs' and options.gui != 'y':
	if options.target_cluster == None or options.scale_direct == None:
		print('-c and -d are necessary for reconfig single cluster without GUI')
		exit()
	elif options.scale_direct != 'a' and options.scale_direct != 'd':
		print('-d option should be \'a\' for adding, or \'d\' for decreasing')
		exit()
print('debug: options:')
print(options)
#print('debug: mode= ' + mode)


#----- check key file -----
providers = []

# key file not existed
if not os.path.exists(options.key_file):
	print('debug: key file not existed')
	if options.gui == 'y':
		get_keys.get_keys(False, options.key_file)
	else:
		print('Error: Please edit or specify the key file to provide keys')
	exit()

# key file existed
providers = get_keys.get_keys(True, options.key_file)
if providers == None:
	print('Error: No valid provider')
	exit()

#..... key file existed .....

#----- get nodes -----
allnode, alllb, allimage = get_nodes.get_nodes(options.key_file, providers)
if len(allnode) < 1:
	print('Error: No node')
	exit()
if len(alllb) < 1:
	print('Warning: No loadbalancer')

#..... get nodes and load balancers .....

#----- Beginning mode -----
if options.mode == 'b' or not os.path.exists(options.config_file):
	print('debug: Beginning Mode')
	# cluntering with GUI
	if options.gui == 'y':
		guithread = gui_cluster.GUI_Thread_Cluster(allnode, alllb, options.config_file, allimage)
		guithread.setDaemon(True)
		print('debug: starting GUI')
		guithread.start()
		guithread.join()
		if not os.path.exists(options.config_file):
			print('Error: specified config file ' + options.config_file + ' not generated')
			exit()
	# generate an simplest config xml file for user to cluster
	else:
		system = chris.System('Chris', [])
		for node in allnode:
			if node.extra['status'] != 'stopped' and node.extra['status'] != 'running':
				system.pending_nodes.append(node)
			else:
				# name, mynodes, scaletype, amount, running_max, loadbalancer
				system.clusters.append(chris.Cluster(node.name, [node]))
				system.clusters[len(system.clusters)-1].check_running()
				system.clusters[len(system.clusters)-1].amount = 1
#		print('debug: clusters = ' + str(len(system.clusters)))
#		print('debug: pending_nodes = ' + str(len(system.pending_nodes)))
		system.generate_xml(options.config_file)
		print('The configuration file has been generated as ' + options.config_file)
	exit()

#..... clustering/config file existed .....

#----- Construct the system tree with the config file-----
tree = ET.parse(options.config_file)
root = tree.getroot()
#print('debug: finish parsing')
if str(root.tag) != 'SYSTEM':
	print('Error: syntax error in configuration xml file: <SYSTEM>: not ' + root.tag)
	print('All changes discarded')
	exit()

if options.mode == 'u':
	print('debug: Update Mode')
	system = chris.System(root.attrib['name'], [])
#	print('debug: reconfig 1st stage')
	if not system.reconfig(root, False, allnode, options, alllb):
		print("debug: reconfig 1st stage not completed")
		exit()
	system.generate_xml(options.config_file)
	print("debug: The file " + options.config_file + ' has been updated')
	exit()

#elif options.mode == 'rx':
#	print('debug: ReconfigXML Mode')
#	print('debug: reconfig 1st stage')
#	if not system.reconfig(root, False, allnode, options, alllb):
#		print("debug: reconfig 1st stage not completed")
#		exit()

elif options.mode == 'rs':
	print('debug: ReconfigSingle Mode')
	system = chris.System(root.attrib['name'], [])
	
	options.mode = 'u'
#	print('debug: reconfig 1st stage')
	if not system.reconfig(root, False, allnode, options, alllb):
		print("debug: reconfig 1st stage not completed")
		exit()
	
	#..... System data structure was established .....
	
	system.generate_xml(options.config_file)
	print("debug: The file " + options.config_file + ' has been updated')
	options.mode = 'rs'
	
	#..... input config file was been updated .....
	
	# activate GUI
	if options.gui == 'y':
		guithread = gui_reconfigsingle.GUI_Thread_ReconfigSingle(options, system, allnode, alllb)
		guithread.setDaemon(True)
		print('debug: starting GUI')
		guithread.start()
		guithread.join()
	# command line
	else:
		if not reconfig_single.reconfig_single(options, system, allnode, alllb):
			print('Error: reconfig single cluster')
			exit()

#..... temp config file was been generated .....
# --- The moves before this would not cause any actual change to the system on the cloud, jusy malnipulate the temp file --- 

#----- Reconfiguration -----
tree = ET.parse('configuration.tmp.xml')
root = tree.getroot()
#print('debug: finish parsing')
if str(root.tag) != 'SYSTEM':
	print('Error: syntax error in reconfiguration.xml: <SYSTEM>: not ' + root.tag)
	print('All changes discarded')
	exit()

system = chris.System(root.attrib['name'], [])

print('debug: reconfig 2nd stage')

allnode, alllb, allimage = get_nodes.get_nodes(options.key_file, providers)

if not system.reconfig(root, True, allnode, options, alllb): # This would cause the real modification on the system
	print('Error: Reconfig Failed')
	print('Warning: This faile might already cause some changes to the system')
	exit()

print('debug: Reconfig succeed')
allnode, alllb, allimage = get_nodes.get_nodes(options.key_file, providers)
system.update_status(allnode)
system.generate_xml(options.config_file)

print('debug: The system configuration and status agree with the description of ' + options.config_file)
exit()
