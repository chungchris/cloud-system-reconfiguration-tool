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
## GUI for user to do clustering
###########################################################################

from threading import Thread
import wx
import wx.xrc

import myheader as chris


class ClusterGuiobj:
	def __init__(self):
		self.name_guiobj = None
		self.scale_type_guiobj = None
		self.lb_guiobj = None
		self.image_guiobj = None
		self.ini_script_guiobj = None
		self.running_max_guiobj = None
		self.nodes_guiobj_checkbox = []


class Clustering(wx.Frame):
	def __init__(self, parent, allnode, alllb, config_file, images):
		CLUSTERS = len(allnode)
		self.node_info = []
		self.alllb = alllb
		self.config_file = config_file
		self.clusters = []
		self.images = images
		
		for node in allnode:
			info = dict({'node':node, 'name':str(node.name), 'id':str(node.id), 'provider':str(node.driver.name), 'region':str(node.extra['availability']), 'type':str(node.extra['instance_type']), 'status':str(node.extra['status'])})
			self.node_info.append(info)
		print('debug: node_info: ' + str(len(self.node_info)))
		
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RC Clustering", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		#self.SetSizeHintsSz( wx.Size(900, -1), wx.DefaultSize )
		
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		#fgSizer1.SetMinSize(wx.Size(800, -1))
		
		fgSizer11 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"System Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		fgSizer11.Add( self.m_staticText111, 0, wx.ALL, 5 )
		
		self.m_textCtrl112 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer11.Add( self.m_textCtrl112, 0, wx.ALL, 5 )
		
		fgSizer1.Add( fgSizer11, 1, wx.EXPAND, 5 )
		
		fgSizer12 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText121 = wx.StaticText( self, wx.ID_ANY, u"Clusters", wx.DefaultPosition, wx.Size( 800,-1 ), 0 )
		self.m_staticText121.Wrap( -1 )
		fgSizer12.Add( self.m_staticText121, 0, wx.ALL, 5 )
		
		self.m_button122 = wx.Button( self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_button122, 0, wx.ALL, 5 )
		
		fgSizer1.Add( fgSizer12, 1, wx.EXPAND, 5 )
		
		self.m_scrolledWindow13 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow13.SetScrollRate( 5, 5 )
		self.m_scrolledWindow13.SetMinSize(wx.Size(-1, 400))
		fgSizer13 = wx.FlexGridSizer( 0, 1, 15, 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		#fgSizer13.SetMinSize(wx.Size(-1, 450))
		
		for i in range(1, CLUSTERS + 1):
			cluster = ClusterGuiobj()
		
			fgSizer131 = wx.FlexGridSizer( 0, 4, 0, 0 )
			fgSizer131.SetFlexibleDirection( wx.BOTH )
			fgSizer131.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
			self.m_staticText21 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, str(i), wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText21.Wrap( -1 )
			fgSizer131.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
			fgSizer22 = wx.FlexGridSizer( 0, 1, 0, 0 )
			fgSizer22.SetFlexibleDirection( wx.BOTH )
			fgSizer22.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
			self.m_staticText221 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText221.Wrap( -1 )
			fgSizer22.Add( self.m_staticText221, 0, wx.ALL, 5 )
		
			self.m_textCtrl222 = wx.TextCtrl( self.m_scrolledWindow13, wx.ID_ANY, allnode[i-1].name, wx.DefaultPosition, wx.DefaultSize, 0 )
			fgSizer22.Add( self.m_textCtrl222, 0, wx.ALL, 5 )
			cluster.name_guiobj = self.m_textCtrl222
		
			fgSizer131.Add( fgSizer22, 1, wx.EXPAND, 5 )
		
			gSizer23 = wx.GridSizer( 0, 2, 0, 0 )
		
			self.m_staticText231 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Scale Type", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText231.Wrap( -1 )
			gSizer23.Add( self.m_staticText231, 0, wx.ALL, 5 )
		
			m_choice232Choices = [ u"UP (Vertical)", u"OUT (HORIZONTAL)" ]
			self.m_choice232 = wx.Choice( self.m_scrolledWindow13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice232Choices, 0 )
			self.m_choice232.SetSelection( 0 )
			gSizer23.Add( self.m_choice232, 0, wx.ALL, 5 )
			cluster.scale_type_guiobj = self.m_choice232
		
			self.m_staticText233 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Load Balancer", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText233.Wrap( -1 )
			gSizer23.Add( self.m_staticText233, 0, wx.ALL, 5 )
		
			m_choice234Choices = [ lb.name for lb in alllb ]
			self.m_choice234 = wx.Choice( self.m_scrolledWindow13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice234Choices, 0 )
			self.m_choice234.SetSelection( 0 )
			gSizer23.Add( self.m_choice234, 0, wx.ALL, 5 )
			cluster.lb_guiobj = self.m_choice234
			
			self.m_staticText233 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Image", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText233.Wrap( -1 )
			gSizer23.Add( self.m_staticText233, 0, wx.ALL, 5 )
		
			ttt = [ str(image.name) for image in images ]
			m_choice234Choices = ['None']
			m_choice234Choices.extend(ttt)
			self.m_choice234 = wx.Choice( self.m_scrolledWindow13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice234Choices, 0 )
			self.m_choice234.SetSelection( 0 )
			gSizer23.Add( self.m_choice234, 0, wx.ALL, 5 )
			cluster.image_guiobj = self.m_choice234
		
			self.m_staticText235 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Initialization Script", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText235.Wrap( -1 )
			gSizer23.Add( self.m_staticText235, 0, wx.ALL, 5 )
		
			self.m_filePicker236 = wx.FilePickerCtrl( self.m_scrolledWindow13, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 150,-1 ), wx.FLP_DEFAULT_STYLE )
			gSizer23.Add( self.m_filePicker236, 0, wx.ALL, 5 )
			cluster.ini_script_guiobj = self.m_filePicker236
		
			self.m_staticText237 = wx.StaticText( self.m_scrolledWindow13, wx.ID_ANY, u"Max Running node", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText237.Wrap( -1 )
			gSizer23.Add( self.m_staticText237, 0, wx.ALL, 5 )
		
			self.m_spinCtrl238 = wx.SpinCtrl( self.m_scrolledWindow13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.SP_ARROW_KEYS, 0, 10, 0 )
			gSizer23.Add( self.m_spinCtrl238, 0, wx.ALL, 5 )
			cluster.running_max_guiobj = self.m_spinCtrl238
		
			fgSizer131.Add( gSizer23, 1, wx.EXPAND, 5 )
		
			self.m_scrolledWindow24 = wx.ScrolledWindow( self.m_scrolledWindow13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
			self.m_scrolledWindow24.SetScrollRate( 5, 5 )
			self.m_scrolledWindow24.SetMinSize(wx.Size(500, -1))
			fgSizer24 = wx.FlexGridSizer( 1, 6, 0, 0 )
			fgSizer24.SetFlexibleDirection( wx.BOTH )
			fgSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
			#fgSizer24.SetMinSize(wx.Size(550, -1))
		
			self.m_staticText241 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"Node", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText241.Wrap( -1 )
			fgSizer24.Add( self.m_staticText241, 0, wx.ALL, 5 )
		
			self.m_staticText242 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"ID", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText242.Wrap( -1 )
			fgSizer24.Add( self.m_staticText242, 0, wx.ALL, 5 )
		
			self.m_staticText243 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"Provider", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText243.Wrap( -1 )
			fgSizer24.Add( self.m_staticText243, 0, wx.ALL, 5 )
		
			self.m_staticText244 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"Region", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText244.Wrap( -1 )
			fgSizer24.Add( self.m_staticText244, 0, wx.ALL, 5 )
		
			self.m_staticText245 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText245.Wrap( -1 )
			fgSizer24.Add( self.m_staticText245, 0, wx.ALL, 5 )
		
			self.m_staticText246 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText246.Wrap( -1 )
			fgSizer24.Add( self.m_staticText246, 0, wx.ALL, 5 )
		
			for node in self.node_info:
				self.m_checkBox247 = wx.CheckBox( self.m_scrolledWindow24, wx.ID_ANY, node['name'], wx.DefaultPosition, wx.DefaultSize, 0 )
				if self.node_info.index(node) == i-1:
					self.m_checkBox247.SetValue(True)
				fgSizer24.Add( self.m_checkBox247, 0, wx.ALL, 5 )
				cluster.nodes_guiobj_checkbox.append(self.m_checkBox247)
		
				self.m_staticText248 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, node['id'], wx.DefaultPosition, wx.DefaultSize, 0 )
				self.m_staticText248.Wrap( -1 )
				fgSizer24.Add( self.m_staticText248, 0, wx.ALL, 5 )
		
				self.m_staticText249 = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, node['provider'], wx.DefaultPosition, wx.DefaultSize, 0 )
				self.m_staticText249.Wrap( -1 )
				fgSizer24.Add( self.m_staticText249, 0, wx.ALL, 5 )
		
				self.m_staticText24a = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, node['region'], wx.DefaultPosition, wx.DefaultSize, 0 )
				self.m_staticText24a.Wrap( -1 )
				fgSizer24.Add( self.m_staticText24a, 0, wx.ALL, 5 )
		
				self.m_staticText24b = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, node['type'], wx.DefaultPosition, wx.DefaultSize, 0 )
				self.m_staticText24b.Wrap( -1 )
				fgSizer24.Add( self.m_staticText24b, 0, wx.ALL, 5 )
		
				self.m_staticText24c = wx.StaticText( self.m_scrolledWindow24, wx.ID_ANY, node['status'], wx.DefaultPosition, wx.DefaultSize, 0 )
				self.m_staticText24c.Wrap( -1 )
				fgSizer24.Add( self.m_staticText24c, 0, wx.ALL, 5 )
		
			self.m_scrolledWindow24.SetSizer( fgSizer24 )
			self.m_scrolledWindow24.Layout()
			fgSizer24.Fit( self.m_scrolledWindow24 )
			fgSizer131.Add( self.m_scrolledWindow24, 1, wx.EXPAND |wx.ALL, 5 )
		
			fgSizer13.Add( fgSizer131, 1, wx.EXPAND, 5 )
			
			self.clusters.append(cluster)
		
		self.m_scrolledWindow13.SetSizer( fgSizer13 )
		self.m_scrolledWindow13.Layout()
		fgSizer13.Fit( self.m_scrolledWindow13 )
		fgSizer1.Add( self.m_scrolledWindow13, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		fgSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button122.Bind(wx.EVT_BUTTON, self.buttonevent)
		#self.m_button122.Bind(wx.EVT_BUTTON, self.buttonevent)

	def buttonevent(self, event):
		#pass
		mysystem = chris.System(self.m_textCtrl112.GetValue(), []) 
		for cluster in self.clusters:
			if cluster.name_guiobj.IsEmpty():
				continue
			mycluster = chris.Cluster(cluster.name_guiobj.GetValue(), [], ini_script = cluster.ini_script_guiobj.GetPath())
			if cluster.scale_type_guiobj.GetCurrentSelection() == 0:
				mycluster.scaletype = 'UP'
			else:
				mycluster.scaletype = 'OUT'
				mycluster.loadbalancer = self.alllb[cluster.lb_guiobj.GetCurrentSelection()].id
			if cluster.image_guiobj.GetCurrentSelection() != 0:
				mycluster.image = self.images[cluster.image_guiobj.GetCurrentSelection()-1].id
			else:
				mycluster.image = None
			if cluster.running_max_guiobj.GetValue() != 0:
				mycluster.running_max = cluster.running_max_guiobj.GetValue()
			else:
				mycluster.running_max = None
			counter = 0
			node_count = 0
			for node in cluster.nodes_guiobj_checkbox:
				if node.IsChecked():
					mycluster.mynodes.append(self.node_info[counter]['node'])
					node_count = node_count + 1
				counter = counter + 1
			mycluster.amount = node_count
			mycluster.check_running()
			mysystem.clusters.append(mycluster)
			print('debug: GUI defined cluster ' + mycluster.name + ' with ' + str(len(mycluster.mynodes)) + ' nodes')
		if len(mysystem.clusters) < 1:
			print('Warning: No cluster defined. (Each cluster should be assigned with a unique name)')
		else:
			mysystem.generate_xml(self.config_file)
			print('debug: the config file is generated as ' + self.config_file)
		self.Close()

	def __del__( self ):
		pass


class GUI_Cluster(Clustering):
    def __init__(self, parent, allnode, alllb, config_file, images):
        Clustering.__init__(self, parent, allnode, alllb, config_file, images)


class GUI_Thread_Cluster(Thread):
	def __init__(self, allnode, alllb, config_file, image):
		Thread.__init__(self)
		self.app = wx.App(False) #mandatory in wx, create an app, False stands for not deteriction stdin/stdout
		self.config_file = config_file
		self.allnode = allnode
		self.alllb = alllb
		self.images = image
	
	def run(self):
		frame = GUI_Cluster(None, self.allnode, self.alllb, self.config_file, self.images) 
		frame.Show(True)
		self.app.MainLoop()
