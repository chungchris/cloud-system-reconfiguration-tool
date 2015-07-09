# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  6 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
###########################################################################
## Chris @ DCSLAB, NCTU
## gui_key.py
## GUI for user to give keys
###########################################################################

from threading import Thread
#import copy
import xml.etree.ElementTree as ET
import wx
import wx.xrc

import reconfig_single
import myheader as chris
import get_nodes
import get_keys

SCALE_POLICY = [ 'vcpu', 'ram', 'price', 'disk', 'bandwidth' ]

class ReconfigSingle( wx.Frame ):
	
	def __init__(self, parent, options, system, allnode, alllb):
		self.system = system
		self.options = options
		self.allnode = allnode
		self.alllb = alllb
		
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RC Reconfig Single Cluster", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		#self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer1.SetMinSize( wx.Size( 500,-1 ) ) 
		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		self.m_scrolledWindow1.SetMinSize( wx.Size( 900,700 ) )
		
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer1.SetMinSize( wx.Size( 500,-1 ) ) 
		self.m_staticText1 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Reconfig Single Cluster", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 8, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Cluster", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer4.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.m_choice1Choices = [ cluster.name for cluster in system.clusters ]
		self.m_choice1 = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		fgSizer4.Add( self.m_choice1, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Scale Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer4.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		m_choice2Choices = [ u"UP (Vertical)", u"OUT (Horizontal)" ]
		self.m_choice2 = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
		self.m_choice2.SetSelection( 0 )
		fgSizer4.Add( self.m_choice2, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Scale Direct", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer4.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		m_choice3Choices = [ u"Add (Increase)", u"Reduce (Decrease)" ]
		self.m_choice3 = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
		self.m_choice3.SetSelection( 0 )
		fgSizer4.Add( self.m_choice3, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Policy", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		fgSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		m_choice4Choices = SCALE_POLICY
		self.m_choice4 = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice4Choices, 0 )
		self.m_choice4.SetSelection( 0 )
		fgSizer4.Add( self.m_choice4, 0, wx.ALL, 5 )
		
		fgSizer1.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.m_checkBox1 = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"Active Initialization Script", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_checkBox1, 0, wx.ALL, 5 )
		self.m_checkBox1.SetValue(True)
		
		self.m_button1 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Send", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"System", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_button3 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Preview", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button3, 0, wx.ALL, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText10 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Now", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		fgSizer2.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"After Reconfig (Estimated)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		self.m_scrolledWindow2.SetMinSize( wx.Size( 300,300 ) )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_treeCtrl1 = wx.TreeCtrl( self.m_scrolledWindow2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		self.m_treeCtrl1.SetMinSize( wx.Size( 300,300 ) )
		self.tree_generation(self.m_treeCtrl1)
		self.m_treeCtrl1.ExpandAll()
		
		bSizer3.Add( self.m_treeCtrl1, 0, wx.ALL, 5 )
		
		self.m_scrolledWindow2.SetSizer( bSizer3 )
		self.m_scrolledWindow2.Layout()
		bSizer3.Fit( self.m_scrolledWindow2 )
		fgSizer2.Add( self.m_scrolledWindow2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_scrolledWindow3 = wx.ScrolledWindow( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow3.SetScrollRate( 5, 5 )
		self.m_scrolledWindow3.SetMinSize( wx.Size( 300,300 ) )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_treeCtrl2 = wx.TreeCtrl( self.m_scrolledWindow3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		self.m_treeCtrl2.SetMinSize( wx.Size( 300,300 ) )
		self.m_treeCtrl2.ExpandAll()
		
		bSizer4.Add( self.m_treeCtrl2, 0, wx.ALL, 5 )
		
		self.m_scrolledWindow3.SetSizer( bSizer4 )
		self.m_scrolledWindow3.Layout()
		bSizer4.Fit( self.m_scrolledWindow3 )
		fgSizer2.Add( self.m_scrolledWindow3, 1, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )

		self.m_button2 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_scrolledWindow1.SetSizer( fgSizer1 )
		self.m_scrolledWindow1.Layout()
		fgSizer1.Fit( self.m_scrolledWindow1 )
		bSizer1.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button1.Bind(wx.EVT_BUTTON, self.buttonevent)
		self.m_button3.Bind(wx.EVT_BUTTON, self.buttonevent_preview)
		self.m_button2.Bind(wx.EVT_BUTTON, self.buttonevent_update)
	
	def buttonevent(self, event):
		print('debug: Send...')
		#print('debug: ori type: ' + self.system.clusters[1].mynodes[0].extra['instance_type'])
		self.options_generation()
		if not reconfig_single.reconfig_single(self.options, self.system, self.allnode, self.alllb):
			print('Error: reconfig_single()')
			return
		self.Close()
		#tree = ET.parse('configuration.tmp.xml')
		#root = tree.getroot()
		#print('debug: finish parsing')
		#self.system = chris.System(root.attrib['name'], [])
		#if not self.system.reconfig(root, True, self.allnode, self.options, self.alllb): # This would cause the real modification on the system
		#	print('Error: Reconfig Failed')
		#	print('Warning: This faile might already cause some changes to the system')
		#	exit()
		#self.tree_generation(self.m_treeCtrl2)
		#self.m_staticText11.SetLabel("After Reconfig")
		#self.m_staticText10.SetLabel("Original")
	
	def buttonevent_preview(self, event):
		print('debug: Preview...')
		self.options_generation()
		#system_preview = copy.deepcopy(self.system)
		tree = ET.parse(self.options.config_file)
		root = tree.getroot()
		system_preview = chris.System(root.attrib['name'], [])
		allnode, alllb, allimage = get_nodes.get_nodes(self.options.key_file, get_keys.get_keys(True, self.options.key_file))
		system_preview.reconfig(root, False, allnode, self.options, alllb)
		#system_preview.name = 'temp'
		if not reconfig_single.reconfig_single(self.options, system_preview, self.allnode, self.alllb, modifyxml = False):
			print('Error; reconfig_single()')
			return
		tree = ET.parse('configuration.preview.xml')
		root = tree.getroot()
		#print('debug: finish parsing')
		system_preview = chris.System(root.attrib['name'], [])
		if not system_preview.reconfig(root, False, allnode, self.options, alllb, preview = True):
			print('Error: Preview Failed')
			return
		#	#print('Warning: This faile might already cause some changes to the system')
		#	exit()
		print('hi')
		self.tree_generation(self.m_treeCtrl2, system_preview = system_preview)
		self.m_treeCtrl2.ExpandAll()
		self.m_staticText11.SetLabel("After Reconfig (Estimated)")
		self.m_treeCtrl2.Update()
	
	def buttonevent_update(self, event):
		#pass
		print('debug: Update...')
		self.options.mode = 'u'
		#print('debug: reconfig 1st stage')
		tree = ET.parse(self.options.config_file)
		root = tree.getroot()
		self.system = chris.System(root.attrib['name'], [])
		if not self.system.reconfig(root, False, self.allnode, self.options, self.alllb):
			print("debug: reconfig 1st stage not completed")
			exit()
		#..... System data structure was established .....
		self.system.generate_xml(self.options.config_file)
		print("debug: The file " + self.options.config_file + ' has been updated')
		self.options.mode = 'rs'
		self.tree_generation(self.m_treeCtrl1)
		self.m_treeCtrl1.ExpandAll()
		self.m_treeCtrl2.CollapseAll()
		self.m_staticText10.SetLabel("Now")
	
	def options_generation(self):
		self.options.target_cluster = self.m_choice1Choices[self.m_choice1.GetCurrentSelection()]
		if self.m_choice2.GetCurrentSelection() == 0:
			self.options.scale_type = 'up'
		else:
			self.options.scale_type = 'out'
		if self.m_choice3.GetCurrentSelection() == 0:
			self.options.scale_direct = 'a'
		else:
			self.options.scale_direct = 'd'
		scale_policy = SCALE_POLICY[self.m_choice4.GetCurrentSelection()]
		if self.m_checkBox1.IsChecked():
			self.options.active_ini_script == 'y'
		else:
			self.options.active_ini_script == 'n'
	
	def tree_generation(self, treeobj, system_preview = None):
		if system_preview == None:
			systemtree = self.system
		else:
			systemtree = system_preview
		treeobj.CollapseAll()
		tree_root = treeobj.AddRoot(systemtree.name)
		for cluster in systemtree.clusters:
			tree_cluster = treeobj.AppendItem(tree_root, cluster.name + ' (' + cluster.scaletype + ')')
			for node in cluster.mynodes:
				tree_node = treeobj.AppendItem(tree_cluster, node.name + ' (' + node.id + ')')
				treeobj.AppendItem(tree_node, 'TYPE: ' + node.extra['instance_type'])
				treeobj.AppendItem(tree_node, 'STATUS: ' + node.extra['status'])
	
	def __del__( self ):
		pass


class GUI_ReconfigSingle(ReconfigSingle):
    def __init__(self, parent, options, system, allnode, alllb):
        ReconfigSingle.__init__(self, parent, options, system, allnode, alllb)


class GUI_Thread_ReconfigSingle(Thread):
	def __init__(self, options, system, allnode, alllb):
		Thread.__init__(self)
		self.app = wx.App(False) #mandatory in wx, create an app, False stands for not deteriction stdin/stdout
		self.options = options
		self.system = system
		self.allnode = allnode
		self.alllb = alllb
	
	def run(self):
		frame = GUI_ReconfigSingle(None, self.options, self.system, self.allnode, self.alllb) 
		frame.Show(True)
		self.app.MainLoop()
