import sys
import time
import os.path
import operator
from sys import stdin
import thread as oldthread
from fabric.api import env, run, sudo
from fabric.network import disconnect_all
import traceback

def send_script_last_thread(command, host, user, key):
	env.host_string = host
	env.user = user
	env.key_filename = key
	try:
		if 'sudo' in command:
			result = sudo(command)
		else:
			result = run(command)
	except Exception, err:
		print('Warning: exception raise in the thread: ' + str(err))
	#print('debug: script thread sent: ' + command)


class Provider:
	def __init__(self, name, region, id, key, lb):
		self.name = name
		self.region = region
		self.id = id
		self.key = key
		self.lb = lb

#class Loadbalancer:
#	def __init__(self, name, id, key, region):
#		self.name = name
#		self.id = id
#		self.key = key
#		self.region = region

# contain the available sizes from the specific provider(driver)
class SizeDB:	
	def __init__(self, driver):
		try:
			self.sizes = driver.list_sizes()
		except Exception, err:
			print('Error: SizeDB.__init__(): ' + str(err))
			exit()
		self.addvcpu()
		#print(self.sizes)
	
	def addvcpu(self):
		VCPU = {'c1.medium':2, 'c1.xlarge':8, 'c3.large':2, 'c3.xlarge':4, 'c3.2xlarge':8, 'c3.4xlarge':16, 'c3.8xlarge':32, 'c4.large':2, 'c4.xlarge':4, 'c4.2xlarge':8, 'c4.4xlarge':16, 'c4.8xlarge':36, 'cc2.8xlarge':32, 'cg1.4xlarge':16, 'cr1.8xlarge':32, 'd2.xlarge':4, 'd2.2xlarge':8, 'd2.4xlarge':16, 'd2.8xlarge':36, 'g2.2xlarge':8, 'g2.8xlarge':32, 'hi1.4xlarge':16, 'hs1.8xlarge':17, 'i2.xlarge':4, 'i2.2xlarge':8, 'i2.4xlarge':16, 'i2.8xlarge':32, 'm1.small':1, 'm1.medium':1, 'm1.large':2, 'm1.xlarge':4, 'm2.xlarge':2, 'm2.2xlarge':4, 'm2.4xlarge':8, 'm3.large':2, 'm3.medium':1, 'm3.xlarge':4, 'm3.2xlarge':8, 'r3.large':2, 'r3.xlarge':4, 'r3.2xlarge':8, 'r3.4xlarge':16, 'r3.8xlarge':32, 't1.micro':1, 't2.micro':1, 't2.small':1, 't2.medium':2}
		for k in VCPU:
			#print(k + ' corresponds to ' + str(VCPU[k]))
			for size in self.sizes:
				if size.id == k:
					size.extra['vcpu'] = VCPU[k]
		for size in self.sizes:
			if 'vcpu' not in size.extra:
				size.extra['vcpu'] = -1
	
	# input: type name
	# return: size object (None)
	def getsize(self, type):
		for size in self.sizes:
			if size.id == type:
				return size
		return None
	
	# input: a list of "type name" ganna be sorted according to the policy
	# return: a list of size "object" after sorted
	def sort_sizebd(self, list, policy):
		#self.sizes.sort(key=operator.attrgetter(policy), reverse=False) #  sort the database
		new_list = []
		for m in list:
			for size in self.sizes:
				if m == size.id:
					new_list.append(size)
		if policy == 'vcpu':
			self.sizes.sort(key = lambda size : size.extra['vcpu'], reverse = False)
		else:
			new_list.sort(key = operator.attrgetter(policy), reverse = False)
#		print('debug: sorted list:')
#		print(new_list)
		return new_list
	
	# input: original type object and the scaled direction and policy
	# return: the suggested type name (None)
	def suggest(self, ori_type, direction, policy, concession = 0):
		#for size in self.sizes:
		#	if ori_type.id == size.id:
		#		ori_type.extra['vcpu'] = size.extra['vcpu']
		#		break
		if policy == 'vcpu' and ori_type.extra['vcpu'] == -1:
			print('Error: not support scaling the ' + size.id + ' node according to vcpu number')
			return None
		if policy == 'disk' and ori_type.disk == 0:
			print('Error: not support scaling the ' + size.id + ' node according to disk')
			return None
		if policy == 'bandwidth' and ori_type.bandwidth == None:
			print('Error: not support scaling the ' + size.id + ' node according to bandwidth')
			return None
		
		self.sizes.sort(key = operator.attrgetter('price'), reverse = False)
		
		possiblelist = []
		if concession != 0: # remove the ineligible nodes
			for size in self.sizes:
				if policy == 'vcpu':
					if size.extra['vcpu'] != -1:
						if concession == 1:
							if size.ram < ori_type.ram or size.bandwidth < ori_type.bandwidth or size.disk < ori_type.disk:
								continue
						if direction == 'a':
							if size.price > ori_type.price and size.extra['vcpu'] > ori_type.extra['vcpu']:
								possiblelist.append(size)
						else:
							if size.price < ori_type.price and size.extra['vcpu'] < ori_type.extra['vcpu']:
								possiblelist.append(size)
				else:
					if concession == 1 and size.extra['vcpu'] != -1 and ori_type.extra['vcpu'] != -1:
						if size.extra['vcpu'] < ori_type.extra['vcpu']:
							continue
					if policy == 'ram':
						if concession == 1:
							if size.bandwidth < ori_type.bandwidth or size.disk < ori_type.disk:
								continue
						if direction == 'a':
							if size.price > ori_type.price and size.ram > ori_type.ram:
								possiblelist.append(size)
						else:
							if size.price < ori_type.price and size.ram < ori_type.ram:
								possiblelist.append(size)
					elif policy == 'bandwidth':
						if concession == 1:
							if size.ram < ori_type.ram or size.disk < ori_type.disk:
								continue
						if direction == 'a':
							if size.price > ori_type.price and size.bandwidth > ori_type.bandwidth:
								possiblelist.append(size)
						else:
							if size.price < ori_type.price and size.bandwidth < ori_type.bandwidth:
								possiblelist.append(size)
					elif policy == 'disk':
						if concession == 1:
							if size.ram < ori_type.ram or size.bandwidth < ori_type.bandwidth:
								continue
						if direction == 'a':
							if size.price > ori_type.price and size.disk > ori_type.disk:
								possiblelist.append(size)
						else:
							if size.price < ori_type.price and size.disk < ori_type.disk:
								possiblelist.append(size)
		else:
			ori = ori_type.id.split('.')[0]
			#print('debug: ori:' + ori)
			for size in self.sizes:
				#print('debug: size:' + size.id)
				if size.id[0:len(ori)] == ori:
					if policy == 'vcpu':
						if direction == 'a':
							if size.extra['vcpu'] > ori_type.extra['vcpu']:
								possiblelist.append(size)
						else:
							if size.extra['vcpu'] < ori_type.extra['vcpu']:
								possiblelist.append(size)
					elif policy == 'ram':
						#print('debug: ' + size.id + ' ram ' + str(size.ram) + ', ori ram ' + str(ori_type.ram))
						if direction == 'a':
							if size.ram > ori_type.ram:
								possiblelist.append(size)
						else:
							if size.ram < ori_type.ram:
								possiblelist.append(size)
					elif policy == 'bandwidth':
						if direction == 'a':
							if size.bandwidth > ori_type.bandwidth:
								possiblelist.append(size)
						else:
							if size.bandwidth < ori_type.bandwidth:
								possiblelist.append(size)
					elif policy == 'disk':
						if direction == 'a':
							if size.disk > ori_type.disk:
								possiblelist.append(size)
						else:
							if size.disk < ori_type.disk:
								possiblelist.append(size)
		
		if len(possiblelist) == 0:
			if concession == 1:
				print('Error: SizeDB.suggest(): There is no appropriate bigger/smaller instant type')
				return None
			#elif concession == 1:
			#	print('Warning: SizeDB.suggest(): There is no completely appropriate bigger/smaller instant type in the family for the concession level 1')
			#	return self.suggest(ori_type, direction, policy, concession = 2)
			else:
				print('Warning: SizeDB.suggest(): There is no bigger/smaller instant type in the family for the concession level 0')
				return self.suggest(ori_type, direction, policy, concession = 1)
		
		#print('debug: possible sizes are:')
		#print(possiblelist)
		
		# sort the size list according to the specified policy
		if concession == 2:
			possiblelist.sort(key = operator.attrgetter('price'), reverse = True)
		else:
			if policy == 'vcpu':
				if direction == 'a':
					possiblelist.sort(key = lambda size : size.extra['vcpu'], reverse = False)
				else:
					possiblelist.sort(key = lambda size : size.extra['vcpu'], reverse = True)
			else:
				if direction == 'a':
					possiblelist.sort(key = operator.attrgetter(policy), reverse = False)
				else:
					possiblelist.sort(key = operator.attrgetter(policy), reverse = True)
		
		print('debug: suggestion is ' + possiblelist[0].id + ', difference with original type ' + ori_type.id + ' are:')
		if ori_type.extra['vcpu'] != -1:
			print('vcpu: ' + str(possiblelist[0].extra['vcpu'] - ori_type.extra['vcpu']))
		print('ram: ' + str(possiblelist[0].ram - ori_type.ram))
		print('disk: ' + str(possiblelist[0].disk - ori_type.disk))
		if ori_type.bandwidth != None:
			print('bandwidth: ' + str(possiblelist[0].bandwidth - ori_type.bandwidth))
		print('price: ' + str(possiblelist[0].price - ori_type.price))
		return possiblelist[0].id

		
class StateMap:
	def __init__(self):
		self.RUNNING = 0
		self.STOPPED = 5

class Cluster:
	def __init__(self, name, mynodes, scaletype = 'UP', running_max = None, loadbalancer = None, ini_script = None, image = None):
		self.name = name
		#self.driver = driver
		self.mynodes = mynodes
		self.scaletype = scaletype
		self.amount = 0 # the amount of node in this cluster
		self.running = 0 # the amount of "running" node in this cluster from user's expectation
		self.running_max = running_max # the upper limit of the amount of "running" node in this cluster from user's expectation
		self.loadbalancer = loadbalancer
		self.ini_script = ini_script
		self.image = image
	
	# set the self.running according to current cluster state
	def check_running(self):
		self.running = 0
		for node in self.mynodes:
			if node.state == statemap.RUNNING:
				self.running = self.running + 1
#		print('debug: check_running() of cluster ' + self.name + ': ' + str(self.running))
	
	# start the specified number of node in the cluster, if existed node not enough, then clone new
	# return the amount of node been started
	def start_node(self, num, options, alllb, preview = False):
		r = 0
		for node in self.mynodes:
			if num != 0 and node.state == statemap.STOPPED:
				if preview:
					node.extra['status'] = 'running'
					r = r + 1
					num = num - 1
				else:
					if node.driver.ex_start_node(node):
						num = num - 1
						print('Starting node ' + node.name)
						r = r + 1
						self.after_start_node(node, options)
						if not self.reconfig_lb(node, alllb, True):
							print('Error: Cluster.copy_node().reconfig_lb() failed')
							return r
					else:
						print('Error: Cluster.start_node(): Start node failed')
						return r
		if num != 0:
			if preview:
				if self.image == None:
					r = r + self.copy_node(num, alllb, options, preview = preview)
				else:
					r = r + self.create_node(num, alllb, options, preview = preview)
			else:
				if self.image == None:
					print('debug: Cluster.start_node(): evoke copy_node()')
					r = r + self.copy_node(num, alllb, options)
				else:
					print('debug: Cluster.start_node(): evoke create_node()')
					r = r + self.create_node(num, alllb, options)
		return r
	
	# determine whether waiting until running is necessary and further send the ini script
	# return: a node with updated state
	def after_start_node(self, node, options):
		newnode = node
		if options.active_ini_script == 'y' or options.straightforward == 'n':
			try:
				node.driver.wait_until_running([node])
			except:
				print('Error: Cluster.after_start_node(): ' + str(err))
				return newnode
			while True:
				newnode = self.is_node_running(newnode)
				if newnode != None:
					print('debug: ' + newnode.name + ' is running')
					break
				print('wait...')
				time.sleep(5)
			print(node.name + ' has been started')
		else:
			print(node.name + ' is starting')
		if options.active_ini_script == 'y' and self.ini_script != None:
			if self.send_script_to_node(newnode):
				print('debug: Send initialization script succeeded')
			else:
				print('Error: Cluster.after_start_node(): Send initialization script failed')
		return newnode
	
	# use SSH to send script line by line to the specified node
	# return: True/False
	def send_script_to_node(self, node):
		if len(node.public_ips) == 0:
			print('Error: Cluster.send_script_to_node(): Public IP of node is necessary')
			return False
		host = node.public_ips[0]
		try:
			script = open(self.ini_script, 'r')
		except Exception, err:
			print('Error: Cluster.send_script_to_node(): Could not open script file ' + self.ini_script + '- ' + str(err))
			return False
		line = script.readline()
		if 'username' not in line:
			print('Error: Cluster.send_script_to_node(): The first line of script should be username=...')
			return False
		s = line.find('=')
		line = line[s+1:]
		user = line.strip()
		line = script.readline()
		if 'keyfile' not in line:
			print('Error: Cluster.send_script_to_node(): The second line of script should be keyfile=...')
			return False
		s = line.find('=')
		line = line[s+1:]
		key = line.strip()
		if not os.path.exists(key):
			print('Error: The key file ' + key + ' not existed')
			return False
		
		cmds = []
		while True:
			line = script.readline()
			if line == '':
				break
			cmds.append(line)
		script.close()
		
		env.host_string = host
		env.user = user
		env.key_filename = key
		
		l = len(cmds)
		#print('debug: l = ' + str(l))
		c = 0
		for command in cmds:
			c = c + 1
			if c == l:
				try:
					oldthread.start_new_thread(send_script_last_thread, (command, host, user, key, ))
				except Exception, err:
					print('Error: unable to start thread to send the script: ' + str(err))
					return False
				else:
					print('debug: script thread generated')
					time.sleep(15)
					print(' ')
					try:
						disconnect_all()
					except Exception, err:
						print('Warning: as disconnect thread ssh: ' + str(err))
			elif c == 1:
				count = 0
				while(True):
					result = ''
					try:
						if 'sudo' in command:
							result = sudo(command)
						else:
							result = run(command)
					except Exception, err:
						print('Error: Cluster.send_script_to_node(): Cloud not SSH connect the node: ' + str(err))
						count = count + 1
						if ('connect' in str(err)) and (count < 7):
						#if count < 5:
							print('debug: try again...')
							time.sleep(5)
						else:
							break
					else:
						print('debug: script sent: ' + command)
						print('debug: result: ' + str(result))
						break
			else:
				result = ''
				if 'sudo' in command:
					result = sudo(command)
				else:
					result = run(command)
				print('debug: script sent: ' + command)
				print('debug: result: ' + str(result))
		
		return True
	
	# stop the specified number of node in the cluster
	# return the amount of nodes been stopped
	# @@@@@ can smartly choose the specific nodes to close
	# @@@@@ detach the node from loadbalancer
	def stop_node(self, num, alllb, preview = False):
		r = 0
		for node in self.mynodes:
			if num != 0 and node.state == statemap.RUNNING:
				if self.scaletype == 'OUT':
					if not self.reconfig_lb(node, alllb, False):
						print('Warning: detach from load balancer failed')
				if preview == True:
					node.extra['status'] = 'stopped'
					num = num - 1
					r = r + 1
				else:
					if node.driver.ex_stop_node(node):
						print('debug: stopping node ......')
						num = num - 1
						r = r + 1
					else:
						print('Error: Cluster.stop_node(): stop node failed')
						return r
			if num == 0:
				break
		return r
	
	# create nodes by given image 
	# return: the amount of node been created
	def create_node(self, num, alllb, options, preview = False, size = None, copy_node = None):
		if copy_node == None:
			copy_node = self.mynodes[0]
		#print('debug: copied node: ' + str(copy_node.name))
		image = copy_node.driver.get_image(self.image)
		#print('debug: got image of ' + self.image + ': ' + str(image) + ', whose id is: ' + str(image.id))
		sizedb = SizeDB(copy_node.driver)
		#print('debug: sizedb: ' + str(sizedb))
		if size == None:
			print('hi1')
			size = sizedb.getsize(copy_node.extra['instance_type'])
			#print('debug: got size of ' + copy_node.extra['instance_type'] + ': ' + str(size))
		#print('debug: got size of ' + copy_node.extra['instance_type'] + ': ' + str(size) + ', whose id is: ' + str(size.id))
		#exit()
		ts = time.time()
		r = 0
		while(num != 0):
			print('debug: create_node()...')
			while True:
				try:
					newnode = copy_node.driver.create_node(name = copy_node.name + '_' + str(ts), size = size, image = image, ex_keyname = copy_node.extra['key_name'], ex_security_groups = [((copy_node.extra['groups'])[0])['group_name']])
				except Exception, err:
					print('debug: ' + str(err))
					if 'InvalidAMIID.Unavailable' in str(err):
						print('wait...')
						time.sleep(10)
					else:
						print('Error: Cluster.copy_node().create_node(): create node failed- ' + str(err))
						print(traceback.format_exc())
						#print(sys.exc_info()[0])
						return r
				else:
					print('debug: create_node() successed')
					num = num - 1
					r = r + 1
					break
			print('debug: new node: ' + str(newnode))
#				members = [attr for attr in dir(newnode) if not callable(attr) and not attr.startswith("__")]
#				i = 1
#				for member in members:
#					print('\t('+str(i)+'). '+member+': '+str(getattr(newnode, member)))
#					i=i+1
			newnode = self.after_start_node(newnode, options)			
			self.mynodes.append(newnode)
			if not self.reconfig_lb(newnode, alllb, True):
				print('Error: Cluster.copy_node().reconfig_lb() failed')
		return r
	
	# clone new node
	# return: the amount of node been cloned
	def copy_node(self, num, alllb, options, preview = False):
		image = None
		copy_node = None
		ts = time.time()
		r = 0
		for node in self.mynodes:
			if node.state == statemap.STOPPED:
				try:
					image = node.driver.create_image(node, node.name + '_' + str(ts))
				except Exception, err:
					print('debug: create_image() failed-' + str(err))
					continue
				print('debug: creat image successed: ')
				copy_node = node
				if preview:
					copy_node.name = 'clone_' + copy_node.name
					for i in Range(0, num):
						self.mynodes.append(copy_node)
					return num
#				print(image)
				break
		if image == None:
			for node in self.mynodes:
				if node.state == statemap.RUNNING:
					try:
						image = node.driver.create_image(node, node.name + '_' + str(ts))
					except Exception, err:
						print('debug: create_image() failed- ' + str(err))
						continue
					print('debug: creating image ......')
					time.sleep(3)
					copy_node = node
#					print(image)
					break
		if image == None:
			print('Error: Cluster.copy_node(): Creat image failed')
			return r
		else:
			print('debug: image: ' + str(image))
#			members = [attr for attr in dir(image) if not callable(attr) and not attr.startswith("__")]
#			i = 1
#			for member in members:
#				print('\t('+str(i)+'). '+member+': '+str(getattr(image, member)))
#				i=i+1
			while(num != 0):
				sizedb = SizeDB(copy_node.driver)
				print('debug: create_node()...')
				while True:
					try:
						newnode = copy_node.driver.create_node(name = copy_node.name + '_' + str(ts), size = sizedb.getsize(copy_node.extra['instance_type']), image = image, ex_keyname = copy_node.extra['key_name'], ex_security_groups = [((copy_node.extra['groups'])[0])['group_name']])
					except Exception, err:
						print('debug: ' + str(err))
						if 'InvalidAMIID.Unavailable' in str(err):
							print('wait...')
							time.sleep(10)
						else:
							print('Error: Cluster.copy_node().create_node(): create node failed- ' + str(err))
							return r
					else:
						print('debug: create_node() successed')
						num = num - 1
						r = r + 1
						break
				print('debug: new node: ' + str(newnode))
#				members = [attr for attr in dir(newnode) if not callable(attr) and not attr.startswith("__")]
#				i = 1
#				for member in members:
#					print('\t('+str(i)+'). '+member+': '+str(getattr(newnode, member)))
#					i=i+1
				
				newnode = self.after_start_node(newnode, options)			
				self.mynodes.append(newnode)
				if not self.reconfig_lb(newnode, alllb, True):
					print('Error: Cluster.copy_node().reconfig_lb() failed')
			return r
	
	# check is the specified node actually in running or not
	# return: a node with updated state (None)
	def is_node_running(self, node):
		try:
			current_state = node.driver.list_nodes()
		except Exception, err:
			print('Error: Cluster.is_node_running():' + str(err)) 
			return None
		f = None
		for c in current_state:
			if c.id == node.id:
				f = c
				break
		if f != None and f.state == statemap.RUNNING and f.extra['status'] == 'running':
			return f
		else:
			return None
	
	# check is the specified node actually in running or not
	# return: a node with updated state (None)
	def is_node_stopped(self, node):
		try:
			current_state = node.driver.list_nodes()
		except Exception, err:
			print('Error: Cluster.is_node_running():' + str(err)) 
			return None
		f = None
		for c in current_state:
			if c.id == node.id:
				f = c
				break
		if f != None and f.state == statemap.STOPPED and f.extra['status'] == 'stopped':
			return f
		else:
			return None
	
	# attach the new-created node to the cluster's load balancer
	# return True/False
	def reconfig_lb(self, node, alllb, attach):
		for lb in alllb:
			if lb.id == self.loadbalancer:
				try:
					if attach:
						print('debug: load balancer attach node: ' + node.name)
						lb.driver.balancer_attach_compute_node(lb, node)
					else:
						ms = lb.driver.balancer_list_members(lb)
						member = None
						for m in ms:
							if m.id == node.id:
								member = m
								break
						if member != None:
							print('debug: load balancer detach node: ' + str(member))
							lb.driver.balancer_detach_member(lb, member)
				except Exception, err:
					print('Error: Cluster.reconfig_lb().balancer_attach_compute_node(): ' + str(err))
					return False
				print('debug: after lb reconfig:')
				print(lb.driver.balancer_list_members(lb))
				break
		return True
	
	# modify the "type info" of certain node according to the specified policy and direction
	# return True/False
	def resize(self, d, policy):
		# find out the most powerful or weak node in the cluster
		type_list = list([])
		for node in self.mynodes:
			if node.extra['instance_type'] not in type_list:
				type_list.append(node.extra['instance_type'])
		sizedb = SizeDB(self.mynodes[0].driver)
		type_list = sizedb.sort_sizebd(type_list, policy)
		
		ori_type = None
		if d == 'a':
			ori_type = type_list[0]
		elif d == 'd':
			ori_type = type_list[len(type_list) - 1]
		suggest = sizedb.suggest(ori_type, d, policy)
		if suggest == None:
			print('Error: Cluster.resize(): no appropriate size')
			return False
		for node in self.mynodes:
			if node.extra['instance_type'] == ori_type.id:
				node.extra['instance_type'] = suggest
				print('debug: modify the node type of '+ node.name + ' from ' + ori_type.id + ' to ' + suggest + ' in system structure')
				return True
		return False
		
	def handoff(self, node, type, alllb, options):
		#print('debug: nodes length 1: ' + str(len(self.mynodes)))
		sizedb = SizeDB(node.driver)
		if self.create_node(1, alllb, options, preview = False, size = sizedb.getsize(type), copy_node = node) == 1:
			print('debug: handoff(): create node succeed')
		else:
			print('debug: handoff(): create node failed')
			return
		#print('debug: nodes length 2: ' + str(len(self.mynodes)))
		self.reconfig_lb(node, alllb, False)
		print('debug: handoff(): detached original node')
		#print('debug: nodes length 3: ' + str(len(self.mynodes)))
		node.driver.ex_stop_node(node)
		#print('debug: nodes length 4: ' + str(len(self.mynodes)))
		#newnode = None
		#while True:
		#	newnode = self.is_node_stopped(node)
		#	if newnode != None:
		#		print('debug: ' + newnode.name + ' is stopped')
		#		break
		#	print('wait...')
		#	time.sleep(5)
		#print('debug: handoff(): stopped original node')
		#print('debug: nodes:')
		#for node in self.mynodes:
		#	print(node)
		#	print(node.state)
		#	print(node.extra['status'])
		
		#print('debug: node id is: ' + str(node.id))
		#exit()
		#for n in self.mynodes:
		#	print('debug: name: ' + str(n.name))
		#	print('debug: id: ' + str(n.id))
		#	if n.id == node.id:
		#		print('debug: found')
		#		self.mynodes.remove(n)
		#		print('debug: len=' + str(strlen(self.mynodes)))
		#		self.mynodes.append(newnode)
		#		print('debug: len=' + str(strlen(self.mynodes)))
		#		print('debug: appended newnode, whose state is: ' + newnode.extra['status'])
		#		break


class System:
	def __init__(self, name, clusters):
		self.name = name
		self.clusters = clusters
		self.pending_nodes = []
	
	# generate the config description xml file according to the current "system" data structure
	def generate_xml(self, filename):
		configfile = open(filename, 'w')
		configfile.write('<?xml version="1.0"?>\n')
		configfile.write('<!-- Generate Time: ' + time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S") + '-->\n')
		configfile.write('<SYSTEM name="' + self.name + '">\n')
		for cluster in self.clusters:
			configfile.write('\t<CLUSTER name="' + cluster.name + '"> <!--name is necessary-->\n')
			configfile.write('\t\t<SCALETYPE>' + str(cluster.scaletype) + '</SCALETYPE> <!--"OUT" or "UP"-->\n')
			if cluster.image != None:
				configfile.write('\t\t<IMAGE>' + str(cluster.image) + '</IMAGE> <!--Give the based image of the instances in this cluster-->\n')
			else:
				configfile.write('\t\t<!--<IMAGE></IMAGE>-->\n')
			if cluster.scaletype == 'OUT':
				configfile.write('\t\t<LOADBALANCER>' + str(cluster.loadbalancer) + '</LOADBALANCER> <!--Give the name of load-balancer from the same provider-->\n')
			else:
				configfile.write('\t\t<!--<LOADBALANCER></LOADBALANCER>-->\n')
			if cluster.ini_script != None and len(cluster.ini_script) > 0:
				configfile.write('\t\t<INISCRIPT>' + cluster.ini_script + '</INISCRIPT> <!--The  full path of the initialization script as a node is newly created(cloned) or rebooted-->\n')
			else:
				configfile.write('\t\t<!--<INISCRIPT></INISCRIPT>--> <!--The  full path of the initialization script as a node is newly created(cloned) or rebooted-->\n')
			configfile.write('\t\t<NUMBER>'+ str(cluster.amount) + '</NUMBER> <!--Do not Change-->\n')
			configfile.write('\t\t<RUNNING>' + str(cluster.running) + '</RUNNING> <!--How many running node in this cluster from your expectation-->\n')
			if cluster.running_max == None:
				configfile.write('\t\t<!--<RUNNING_MAX></RUNNING_MAX>--> <!--The upper limit of the amount of the running node in this cluster-->\n')
			else:
				configfile.write('\t\t<RUNNING_MAX>' + str(cluster.running_max) + '</RUNNING_MAX> <!--The upper limit of the amount of the running node in this cluster-->\n')
			for node in cluster.mynodes:
				configfile.write('\t\t<NODE name="' + str(node.name) + '" id="' + str(node.id) + '">\n')
				configfile.write('\t\t\t<DRIVER>' + str(node.driver.api_name) + '</DRIVER> <!--All node in a cluster should use the same driver-->\n')
				configfile.write('\t\t\t<TYPE>' + node.extra['instance_type'] + '</TYPE>\n')
				configfile.write('\t\t\t<STATUS>' + node.extra['status'] + '</STATUS>\n')
				configfile.write('\t\t</NODE>\n')
			configfile.write('\t</CLUSTER>\n')
		configfile.write('</SYSTEM>\n\n')
		configfile.write('<!--Pending Nodes-->\n')
		configfile.write('<!--\n')
		for node in self.pending_nodes:
			configfile.write('<NODE name="' + str(node.name) + '" id="' + str(node.id) + '">\n')
			configfile.write('\t<DRIVER>' + str(node.driver.api_name) + '</DRIVER>\n')
			configfile.write('\t<TYPE>' + node.extra['instance_type'] + '</TYPE>\n')
			configfile.write('\t<STATUS>' + node.extra['status'] + '</STATUS>\n')
			configfile.write('</NODE>\n')
		configfile.write('-->')
		configfile.close()
		print('debug: generate_xml() finished')
	
	# update the status of the nodes in the "system" according to their current status
	# return True/False
	def update_status(self, allnewnode): 
		covernodes = []
		for cluster in self.clusters:
			newnodelist = []
			for node in cluster.mynodes:
				find = False
				for newnode in allnewnode:
					if node.id == newnode.id and node.name == newnode.name:
						find = True
						covernodes.append(newnode)
						newnodelist.append(newnode)
						break
				if not find:
					print('Warning: The node ' + node.name + ' in the cluster ' + cluster.name + ' does not exist')
			cluster.mynodes = newnodelist
			cluster.check_running()
			cluster.amount = len(cluster.mynodes)
		self.pending_nodes = [node for node in allnewnode if node not in covernodes]
		return True
	
	# 1st stage: correctly set up the "system" data structure according to the config description xml file and user command in order to finally generate temp config xml file
	# 2nd stage: compare the current "system" data structure with temp config description xml file in order to modify the system
	# return: True/False
	def reconfig(self, root, modify, allnode, options, alllb, preview = False):
		covernodes = []
		for cluster in root:
			if str(cluster.tag) != 'CLUSTER':
				print('Error: syntax error in configuration.xml: <CLUSTER>: not ' + cluster.tag)
				return False
			if len(cluster.attrib['name']) < 1:
				print('Error: syntax error in configuration.xml: <CLUSTER>: attributes name is necessary')
				return False
			newcluster = Cluster(cluster.attrib['name'], [])
			#print('debug!!!: ' + str(len(newcluster.mynodes)))
			node_count = 0 # the amount of nodes listed in the config, and found in the cloud
			mod = 0
			for cluster_info in cluster:
				# <NODE>
				if cluster_info.tag == 'NODE':
					# use node name and node id to identify a unique node
					find_node = -1
					for node in allnode:
						if node.name == cluster_info.attrib['name'] and node.id == cluster_info.attrib['id']:
							find_node = allnode.index(node)
							break
					if find_node == -1:
						print('Warning: in config file: <NODE>: no node name ' + cluster_info.attrib['name'] + ' with id ' + cluster_info.attrib['id'])
						continue
					node_count = node_count + 1
					skip = False
					for node_info in cluster_info:
						# <DRIVER>
						if node_info.tag == 'DRIVER':
							if str(allnode[find_node].driver.api_name) != node_info.text:
								print('Warning: The driver of ' + cluster_info.attrib['name'] + ' was been corrected to ' + allnode[find_node].driver.api_name)
								#print('Error: syntax error in reconfiguration.xml: <PROVIDER>: provider should be ' + str(allnode[find_node].driver.api_name))
								#exit()
							# check if every node in the cluster comes from the same provider
							#if newcluster.driver != allnode[find_node].driver.api_name:
							#	print('Error: The nodes in a single cluster should come from the provider ' + newcluster.provider)
							#	print('All changes discarded')
							#	exit()
						# <TYPE>
						elif node_info.tag == 'TYPE' and allnode[find_node].extra['instance_type'] != node_info.text and options.mode != 'u':
							# check if the wanted size is available
							sizedb = SizeDB(allnode[find_node].driver)
							if len([size for size in sizedb.sizes if size.id == node_info.text]) == 0:
								print('Error: no type named ' + node_info.text + ' is available from the provider ' + allnode[find_node].driver.name)
								print('y- keep the original type')
								print('l- list all available type')
								print('q- quit')
								print('? ')
								x = stdin.readline()
								x = x.rstrip()
								if str(x) == 'y':
									node_info.text = allnode[find_node].extra['instance_type']
								elif str(x) == 'l':
									for size in sizedb.sizes:
										print('- ' + str(size))
									while True:
										print('The type you want is? (Give the type id, or \'r\' for keep the original type, or \'q\' for quit)')
										userinput = stdin.readline()
										userinput = userinput.rstrip()
										if userinput == 'q':
											return False
										if userinput == 'r':
											node_info.text = allnode[find_node].extra['instance_type']
											break
										else:
											find = False
											for size in sizedb.sizes:
												if userinput == size.id:
													find = True
													node_info.text = size.id
													print('Your input type has been changed to ' + size.id)
													break
											if not find:
												print('Error: no type ' + userinput + ' from the provider ' + allnode[find_node].driver.name)
											else:
												break
								else:
									return False
							if allnode[find_node].extra['instance_type'] == node_info.text:
								pass
							# 2nd stage
							elif modify:
								if preview == True:
									allnode[find_node].extra['instance_type'] = node_info.text
								else:
									handoff = None
									if options.handoff == 'y' and newcluster.image != None:
										handoff = True
									else:
										handoff = False
									
									restart = False
									while(handoff==False):
										try:
											r = allnode[find_node].driver.ex_change_node_size(node, sizedb.getsize(node_info.text))
										except Exception, err:
											print(err)
											if 'InvalidParameterCombination' in str(err): # not support such type changing
												print('Warning: not support such type changing to ' + node_info.text + ', retry...')
												node_info.text = sizedb.suggest(sizedb.getsize(node_info.text), options.scale_direct, options.scale_policy)
												if node_info.text == None:
													print('debug: modify type fail1: ' + str(allnode[find_node].name) + ' from type ' + str(allnode[find_node].extra['instance_type']) + ' to type ' + str(node_info.text))
													return False
												print('try ' + node_info.text)
											elif 'IncorrectInstanceState' in str(err): # the istance should be stopped first
												print('Warning: Stopping the node ' + allnode[find_node].name)
												if newcluster.scaletype == 'OUT':
													if not newcluster.reconfig_lb(allnode[find_node], alllb, False):
														print('Warning: detach from load balancer failed')
												if not allnode[find_node].driver.ex_stop_node(allnode[find_node]):
													print('Error: Stopping node failed')
													return False
												else:
													while(newcluster.is_node_stopped(allnode[find_node]) == None):
														print('wait...')
														time.sleep(5)
														continue
													restart = True
											else:
												print('debug: modify type fail2: ' + allnode[find_node].name + ' from type ' + allnode[find_node].extra['instance_type'] + ' to type ' + node_info.text)
												return False
										else:
											if r:
												print('debug: modify type success: ' + allnode[find_node].name + ' from type ' + allnode[find_node].extra['instance_type'] + ' to type ' + node_info.text)
												if restart:
													if allnode[find_node].driver.ex_start_node(allnode[find_node]):
														print('Starting ' + allnode[find_node].name + ' ......')
														allnode[find_node] = newcluster.after_start_node(allnode[find_node], options)
														if newcluster.scaletype == 'OUT':
															if not newcluster.reconfig_lb(allnode[find_node], alllb, True):
																print('Error: Cluster.reconfig().reconfig_lb() failed')
																return False
														break
													else:
														print('Start ' + cluster_info.attrib['name'] + ' failed')
														return False
											else:
												print('debug: modify type fail3: ' + allnode[find_node].name + ' from type ' + allnode[find_node].extra['instance_type'] + ' to type ' + node_info.text)
												return False
											break
									if handoff:
										print('debug: handoff vertically scaling')
										newcluster.handoff(allnode[find_node], node_info.text, alllb, options)
										while True:
											tnode = newcluster.is_node_stopped(allnode[find_node])
											if tnode != None:
												print('debug: ' + tnode.name + ' is stopped')
												allnode[find_node] = tnode
												break
											print('wait...')
											time.sleep(5)
										print('debug: handoff(): stopped original node')
										skip = True
										
							# 1st stage
							else:
								#x = ''
								#if options.auto == 'y':
								#	x = 'y'
								#else:
								#	print('Given type does not match the original type. Do you want to change ' + allnode[find_node].name + ' from type ' + allnode[find_node].extra['instance_type'] + ' to type ' + node_info.text+' ? (y/n/q): ')
								#	x = stdin.readline()
								#	x = x.rstrip()
								#if str(x) == 'y':
								allnode[find_node].extra['instance_type'] = node_info.text
								#elif str(x) == 'n':
								#	print('Type not changed')
								#else:
								#	return False
						# <STATUS>
						elif node_info.tag == 'STATUS' and allnode[find_node].extra['status'] != node_info.text and options.mode != 'u' and skip == False:
							#states = allnode[find_node].driver.NODE_STATE_MAP
							if node_info.text != 'stopped' and node_info.text != 'running':
								print('Error: Only support status stopped or running')
								return False
							# 2nd stage
							if modify:
								if node_info.text == 'running':
									if allnode[find_node].driver.ex_start_node(allnode[find_node]):
										print('Starting ' + cluster_info.attrib['name'] + ' ......')
										allnode[find_node] = newcluster.after_start_node(allnode[find_node], options)
										if newcluster.scaletype == 'OUT':
											if not newcluster.reconfig_lb(allnode[find_node], alllb, True):
												print('Error: Cluster.reconfig().reconfig_lb() failed')
												return False
									else:
										print('Start ' + cluster_info.attrib['name'] + ' failed')
										return False
								elif node_info.text == 'stopped':
									if newcluster.scaletype == 'OUT':
										if not newcluster.reconfig_lb(allnode[find_node], alllb, False):
											print('Warning: detach from load balancer failed')
									if allnode[find_node].driver.ex_stop_node(allnode[find_node]):
										print('Stop ' + cluster_info.attrib['name'] + ' successed')
									else:
										print('Stop ' + cluster_info.attrib['name'] + ' failed')
										return False
							# 1st stage
							else:
								x = ''
								if options.auto == 'y':
									x = 'y'
								else:
									print('Status not match. Do you want to change ' + allnode[find_node].name + ' from status ' + allnode[find_node].extra['status'] + ' to status ' + node_info.text + ' ? (y/n/q): ')
									x = stdin.readline()
									x = x.rstrip()
								if str(x) == 'y':
									allnode[find_node].extra['status'] = node_info.text
									if node_info.text == 'running':
										mod = mod + 1
									elif node_info.text == 'stopped':
										mod = mod - 1
#									print('mod1: '+str(mod))
								elif str(x) == 'n':
									print('Status not changed')
								else:
									return False
						#else:
						#	print('Warning: tag not supported: ' + node_info.tag)
					
					newcluster.mynodes.append(allnode[find_node])
					#print('debug!!!: ' + str(len(newcluster.mynodes)))
					covernodes.append(allnode[find_node])
				# <SCALETYPE>
				elif cluster_info.tag == 'SCALETYPE':
					if cluster_info.text != 'UP' and cluster_info.text != 'OUT':
						print('Error: syntax error in reconfiguration.xml: <SCALETYPE>: not UP or OUT')
						print('All changes discarded')
						exit()
					newcluster.scaletype = cluster_info.text
				# <IMAGE>
				elif cluster_info.tag == 'IMAGE' and len(cluster_info.text) > 0:
					newcluster.image = cluster_info.text
				# <LOADBALANCER>
				elif cluster_info.tag == 'LOADBALANCER' and len(cluster_info.text) > 0:
					newcluster.loadbalancer = cluster_info.text
				# <RUNNING> the amount of "running" node in this cluster from user's expectation
				elif cluster_info.tag == 'RUNNING':
					if (not cluster_info.text.isdigit()) or int(cluster_info.text) < 0:
						print('Error: syntax error in reconfiguration.xml: <RUNNING>: should be a positive integer number')
						return False
					newcluster.running = int(cluster_info.text)
				# <RUNNING_MAX> the upper limit of the amount of "running" node in this cluster from user's expectation
				elif cluster_info.tag == 'RUNNING_MAX':
					if int(cluster_info.text) <= 0:
						newcluster.running_max = None
					else:
						newcluster.running_max = int(cluster_info.text)
				# <INISCRIPT>
				elif cluster_info.tag == 'INISCRIPT' and len(cluster_info.text) > 0:
					if not os.path.exists(cluster_info.text):
						print('Error: The script ' + cluster_info.text + ' not existed')
						return False
					newcluster.ini_script = cluster_info.text
				# Warning: tag not supported
				else:
					if cluster_info.tag != 'NUMBER':
						print('Warning: tag not supported: ' + cluster_info.tag)
			# set default value if not provided
			if len(newcluster.mynodes) == 0:
				print('Error: There should be at least one node in the cluster ' + newcluster.name)
				return False
			
			self.pending_nodes = [n for n in allnode if n not in covernodes]
			
			#if newcluster.scaletype == None:
			#	newcluster.scaletype = 'UP'
			#	print('Warning: Set Scale Type of the cluster ' + newcluster.name + ' as default value UP')
			#if newcluster.running == None:
			#	newcluster.running = newcluster.check_running()
			#	print('Warning: Set Runnung of the cluster ' + newcluster.name + ' as current value ' + str(newcluster.check_running()))
			#if newcluster.running_max == None:
			#	newcluster.running_max = -1
			#	print('Warning: Set Runnung_Max of the cluster ' + newcluster.name + ' as default value -1')
			
			# check load-balancer
			if newcluster.scaletype == 'OUT':
				exist_lb = False
				if newcluster.loadbalancer == None:
					print('There should be a load balancer in the cluster ' + newcluster.name)
				else:
					for lb in alllb:
						if lb.driver.region == newcluster.mynodes[0].driver.region_name and newcluster.loadbalancer == lb.id:
							exist_lb = True
							break
					if not exist_lb:
						print('The load-balancer ' + newcluster.loadbalancer + ' not found')
				if not exist_lb:
					print('l- list all available loadbalancer')
					#print('c- create a loadbalancer (not suggested)')
					print('q- quit')
					print('? ')
					x = stdin.readline()
					x = x.rstrip()
					if str(x) == 'l':
						for lb in alllb:
							if lb.driver.region == newcluster.mynodes[0].driver._region:
								print('- ' + str(lb))
						while True:
							print('The load balancer you want is? (Give the load-balancer name(id), or \'q\' for quit)')
							userinput = stdin.readline()
							userinput = userinput.rstrip()
							if userinput == 'q':
								return False
							else:
								find = False
								for lb in alllb:
									if lb.driver.region == newcluster.mynodes[0].driver.region_name and userinput == lb.id:
										find = True
										newcluster.loadbalancer = lb.id
										break
								if find:
									break
								else:
									print('The load-balancer ' + lb.id + ' not found')
					#elif tr(x) == 'c':
					else:
						return False
			
			expect_running = newcluster.running
			newcluster.check_running()
			newcluster.running = newcluster.running + mod
			if newcluster.running_max != None and (newcluster.running > newcluster.running_max or expect_running > newcluster.running_max):
				print('Error: Running node exceeds running_max')
				return False
			# check if adjust amount of running node needed
			if newcluster.running != expect_running and options.mode != 'u':
				print('debug: number of running node different: expected is ' + str(expect_running) + ', while # node in running is: ' + str(newcluster.running) )
				# 2nd stage
				if modify:
					# stop some nodes
					if expect_running < newcluster.running:
						s = newcluster.stop_node(newcluster.running - expect_running, alllb, preview = preview)
						if  s  == (newcluster.running - expect_running):
							print('debug: Stopped ' + str(s) + ' node')
						else:
							print('Error: Stopped ' + str(s) + ' node')
					# start some nodes
					else:
						s = newcluster.start_node(expect_running - newcluster.running, options, alllb, preview = preview)
						if  s  == (expect_running - newcluster.running):
							print('debug: Started ' + str(s) + ' node')
						else:
							print('Error: Started ' + str(s) + ' node')
				# 1st stage
				else:
					#x = ''
					#if options.auto == 'y':
					#	x = 'y'
					#else:
					#	print('Do you want to scale cluster ' + cluster.attrib['name'] + ' from '+ str(newcluster.running) + ' in running to ' + str(expect_running) + ' in running? (y/n): ')
					#	x = stdin.readline()
					#	x = x.rstrip()
					#if str(x) == 'y':
					mod = expect_running - newcluster.running
					newcluster.running = expect_running
					if newcluster.running_max != None and (newcluster.running > newcluster.running_max or expect_running > newcluster.running_max):
						print('Error: Running node exceeds running_max')
						return False
					#else:
					#	print('The amount of running node in this cluster was not changed')
			
			newcluster.amount = max(newcluster.running, node_count)
			self.clusters.append(newcluster)
		
		return True

statemap = StateMap()
			
#		print('debug: system tree:')
#		print('debug: clusters = ' + str(len(system.clusters)))
#		i = 1
#		for c in system.clusters:
#			print('\t (' + str(i) + '): ' + str(len(c.mynodes)))
#			i = i + 1
#		print('debug: pending_nodes = ' + str(len(system.pending_nodes)))
