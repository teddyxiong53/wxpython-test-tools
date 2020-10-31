import wx

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="xx", size=(800,600))
        panel = wx.Panel(self)
        panel1 = wx.Panel(panel, pos=(0,0), size=(250, wx.EXPAND))
        panel1.SetBackgroundColour("yellow")
        panel2 = wx.Panel(panel, pos=(255,0), size=(wx.EXPAND, wx.EXPAND))
        panel2.SetBackgroundColour("green")

app = wx.App()
frame = MyFrame(None)
frame.Show(True)
app.MainLoop()
