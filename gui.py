import wx 

class HelloFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, -1, "HelloFrame", size=(200, 100)) 
        panel = wx.Panel(self, -1)  #初始化frame
        wx.StaticText(panel, -1, "Hello World", pos=(60, 25)) #設定文字 
         
if __name__ == '__main__':
    app = wx.PySimpleApp()  #建立simple app
    frame = HelloFrame()       #產生自訂frame
    frame.Show(True)            #顯示frame
    app.MainLoop()                #執行app