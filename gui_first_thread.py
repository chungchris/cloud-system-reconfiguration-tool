import wx
import gui_key

class GUI_Key(gui_key.frame_key_input):
    def __init__(self, parent, keyxmlfile):
        gui_key.frame_key_input.__init__(self, parent, keyxmlfile)

class GUIThread_First(Thread):
	def __init__(self, key_file = None, begin_state, allnode = None, alllb = None, config_file = None):
		Thread.__init__(self)
		self.app = wx.App(False) #mandatory in wx, create an app, False stands for not deteriction stdin/stdout
		self.keyxmlfile = key_file
		self.config_file = config_file
		self.begin_state = begin_state
		self.allnode = allnode
		self.alllb = alllb
	
	def run(self):
		#create an object of CalcFrame
		frame = None
		if self.begin_state == 'key':
			frame = GUI_Key(None, self.keyxmlfile) 
		elif self.begin_state == 'cluster':
			frame = GUI_Cluster(None, self.allnode, self.alllb, self.config_file)
		elif self.begin_state == 'reconfig':
			frame = GUI_Reconfig(None, self.allnode, self.alllb, self.config_file)
		frame.Show(True) #show the frame
		#self.app.SetExitOnFrameDelete(False)
		self.app.MainLoop() #start the applications

