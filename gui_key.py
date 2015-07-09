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

import wx
import wx.xrc
import time
from threading import Thread

Provider_Choices = ["Amazon EC2", "Google Application Engine", "Azure", "Rackspace"]
Region_Choices_AMAZON = ["AMAZON_US_EAST", "AMAZON_US_WEST", "AMAZON_US_WEST_OREGON", "AMAZON_EU_WEST", "AMAZON_AP_SOUTHEAST", "AMAZON_AP_SOUTHEAST_SYDNEY", "AMAZON_AP_NORTHEAST", "AMAZON_SA_EAST"]
region_dir = {"AMAZON_US_EAST":'us-east-1', "AMAZON_US_WEST":'us-west-1', "AMAZON_US_WEST_OREGON":'us-west-2', "AMAZON_EU_WEST":'eu-west-1', "AMAZON_AP_SOUTHEAST":'ap-southeast-1', "AMAZON_AP_SOUTHEAST_SYDNEY":'ap-southeast-2', "AMAZON_AP_NORTHEAST":'ap-northeast-1', "AMAZON_SA_EAST":'sa-east-1'}
Region_Choices_GCE = ['']
Region_Choices_Azure = ['']
Region_Choices_Rackspace = ['']
provider_count_max = 4

class GUI_Provider:
	def __init__(self):
		self.provider_guiobj = None
		self.provider = None
		self.region_guiobj = None
		self.region = None
		self.accessid_guiobj = None
		self.accessid = None
		self.secretkey_guiobj = None
		self.secretkey = None
		self.Region_Choices = []


class Get_Keys(wx.Frame):
	def __init__(self, parent, keyxmlfile):
		self.keyxmlfile = keyxmlfile
		#self.configfile = configfile
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"RC key", pos = wx.DefaultPosition, size = wx.Size( 600,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		bSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button_send = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer.Add( self.m_button_send, 0, wx.ALL, 5 )
		
		self.m_scrolledWindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow.SetScrollRate( 5, 5 )
		fgSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.gui_providers = []
		count = 0
		
		while count < provider_count_max:
			count = count + 1
			gui_provider = GUI_Provider()
		
			self.m_staticText1 = wx.StaticText( self.m_scrolledWindow, wx.ID_ANY, str(count), wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText1.Wrap( -1 )
			fgSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
			fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
			fgSizer1.SetFlexibleDirection( wx.BOTH )
			fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
			self.m_staticText11 = wx.StaticText( self.m_scrolledWindow, wx.ID_ANY, u"Provider", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText11.Wrap( -1 )
			fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
			#m_choice11Choices = [ u"Amazon EC2", u"Google Application Engine", u"Azure", u"Rackspace" ]
			self.m_choice11 = wx.Choice( self.m_scrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Provider_Choices, 0 )
			self.m_choice11.SetSelection( (count-1)%provider_count_max )
			fgSizer1.Add( self.m_choice11, 0, wx.ALL, 5 )
			gui_provider.provider_guiobj = self.m_choice11
			
			self.m_staticText12 = wx.StaticText( self.m_scrolledWindow, wx.ID_ANY, u"Region", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText12.Wrap( -1 )
			fgSizer1.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
			#m_choice12Choices = [ u"AMAZON_US_EAST", u"AMAZON_US_WEST", u"US_WEST_OREGON", u"EU_WEST", u"AP_SOUTHEAST", u"AP_SOUTHEAST_SYDNEY", u"AP_NORTHEAST", u"SA_EAST", u"AP_SOUTHEAST2", u"AMAZON_AP_SOUTHEAST2", u"AMAZON_SA_EAST", u"AMAZON_AP_NORTHEAST", u"AMAZON_AP_SOUTHEAST_SYDNEY", u"AMAZON_AP_SOUTHEAST", u"AMAZON_EU_WEST" ]
			p = self.m_choice11.GetCurrentSelection()
			if p == 0:
				gui_provider.Region_Choices = Region_Choices_AMAZON
			elif p == 1:
				gui_provider.Region_Choices = Region_Choices_GCE
			elif p == 2:
				gui_provider.Region_Choices = Region_Choices_Azure
			else:
				gui_provider.Region_Choices = Region_Choices_Rackspace
			
			self.m_choice12 = wx.Choice( self.m_scrolledWindow, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, gui_provider.Region_Choices, 0 )
			self.m_choice12.SetSelection( 0 )
			fgSizer1.Add( self.m_choice12, 0, wx.ALL, 5 )
			gui_provider.region_guiobj = self.m_choice12
		
			self.m_staticText13 = wx.StaticText( self.m_scrolledWindow, wx.ID_ANY, u"Access ID", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText13.Wrap( -1 )
			fgSizer1.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
			self.m_textCtrl11 = wx.TextCtrl( self.m_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
			fgSizer1.Add( self.m_textCtrl11, 0, wx.ALL, 5 )
			gui_provider.accessid_guiobj = self.m_textCtrl11
		
			self.m_staticText14 = wx.StaticText( self.m_scrolledWindow, wx.ID_ANY, u"Secret Key", wx.DefaultPosition, wx.DefaultSize, 0 )
			self.m_staticText14.Wrap( -1 )
			fgSizer1.Add( self.m_staticText14, 0, wx.ALL, 5 )
		
			self.m_textCtrl12 = wx.TextCtrl( self.m_scrolledWindow, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
			fgSizer1.Add( self.m_textCtrl12, 0, wx.ALL, 5 )
			gui_provider.secretkey_guiobj = self.m_textCtrl12
		
			fgSizer.Add( fgSizer1, 1, wx.EXPAND, 5 )
			
			self.gui_providers.append(gui_provider)
		
		self.m_scrolledWindow.SetSizer( fgSizer )
		self.m_scrolledWindow.Layout()
		fgSizer.Fit( self.m_scrolledWindow )
		bSizer.Add( self.m_scrolledWindow, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button_send.Bind( wx.EVT_BUTTON, self.buttonevent )
	
	def __del__( self ):
		pass
	
	def providertranslation(self, ori_pro, ori_reg):
		provider = ''
		region = ''
		if ori_pro == 'Amazon EC2':
			provider = 'EC2'
			region = region_dir[ori_reg]
		return (provider, region)
		
	# Virtual event handlers, overide them in your derived class
	def buttonevent(self, event):
		#print('debug: ')
		new_gui_providers = []
		for gui_provider in self.gui_providers:
			gui_provider.provider = Provider_Choices[gui_provider.provider_guiobj.GetCurrentSelection()]
			gui_provider.region = gui_provider.Region_Choices[gui_provider.region_guiobj.GetCurrentSelection()]
			gui_provider.provider, gui_provider.region = self.providertranslation(gui_provider.provider, gui_provider.region)
			gui_provider.accessid = gui_provider.accessid_guiobj.GetValue()
			gui_provider.secretkey = gui_provider.secretkey_guiobj.GetValue()
			if len(gui_provider.accessid) < 1 or len(gui_provider.secretkey) < 1:
				break
			new_gui_providers.append(gui_provider)
			#print('debug:')
			#print('\tprovider: ' + gui_provider.provider)
			#print('\tregion: ' + gui_provider.region)
			#print('\taccess id: ' + gui_provider.accessid)
			#print('\tsecreat key: ' + gui_provider.secretkey)
		self.gui_providers = new_gui_providers
		#print('debug: ' + str(len(self.gui_providers)) + ' totally')
		self.generate_xml()
		#self.Show(False)
		self.Close()
		#allnode, alllb = get_nodes.get_nodes(self.keyxmlfile)
		#guithread = gui_cluster.GUI_Thread_Cluster(allnode, alllb, self.configfile)
		#guithread.setDaemon(True)
		#guithread.start()
		#print('debug: start GUI')
		#exit()
		#event.Skip()
	
	def generate_xml(self):
		configfile = open(self.keyxmlfile, 'w')
		configfile.write('<?xml version="1.0"?>\n')
		configfile.write('<!-- Generate Time: ' + time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S") + '-->\n')
		configfile.write('<data>\n')
		for provider in self.gui_providers:
			configfile.write('\t<Provider name="' + str(provider.provider) + '" region="' + str(provider.region) + '">\n')
			configfile.write('\t\t<AccessID>' + str(provider.accessid) + '</AccessID>\n')
			configfile.write('\t\t<SecretKey>' + str(provider.secretkey) + '</SecretKey>\n')
			configfile.write('\t</Provider>\n')
		configfile.write('</data>\n\n')
		configfile.close()
		print('debug: generate_xml() ' + self.keyxmlfile + ' finished')


class GUI_Key(Get_Keys):
    def __init__(self, parent, keyxmlfile):
        Get_Keys.__init__(self, parent, keyxmlfile)

class GUI_Thread_Key(Thread):
	def __init__(self, key_file):
		Thread.__init__(self)
		self.app = wx.App(False) #mandatory in wx, create an app, False stands for not deteriction stdin/stdout
		self.keyxmlfile = key_file
	
	def run(self):
		#create an object of CalcFrame
		frame = GUI_Key(None, self.keyxmlfile) 
		frame.Show(True) #show the frame
		#self.app.SetExitOnFrameDelete(False)
		self.app.MainLoop() #start the applications