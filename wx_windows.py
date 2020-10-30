# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"会议音箱测试程序V1.0", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 800,600 ), wx.Size( 800,600 ) )

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItemExit = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_menuItemExit )

		self.m_menubar1.Append( self.m_menu1, u"文件" )

		self.m_menu3 = wx.Menu()
		self.m_menuItemAbout = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"关于", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItemAbout )

		self.m_menubar1.Append( self.m_menu3, u"帮助" )

		self.SetMenuBar( self.m_menubar1 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		self.m_buttonTestAll = wx.Button( self, wx.ID_ANY, u"一键测试所有", wx.DefaultPosition, wx.Size( 800,50 ), 0 )
		bSizer21.Add( self.m_buttonTestAll, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer21, 1, wx.EXPAND, 5 )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_buttonLeftMic = wx.Button( self, wx.ID_ANY, u"测试左MIC", wx.Point( 50,50 ), wx.Size( 200,120 ), 0 )
		gSizer2.Add( self.m_buttonLeftMic, 0, wx.ALL, 5 )

		self.m_buttonRightMic = wx.Button( self, wx.ID_ANY, u"测试右MIC", wx.DefaultPosition, wx.Size( 200,120 ), 0 )
		gSizer2.Add( self.m_buttonRightMic, 0, wx.ALL, 5 )

		self.m_buttonRef = wx.Button( self, wx.ID_ANY, u"测试REF", wx.DefaultPosition, wx.Size( 200,120 ), 0 )
		gSizer2.Add( self.m_buttonRef, 0, wx.ALL, 5 )

		self.m_buttonAec = wx.Button( self, wx.ID_ANY, u"测试AEC", wx.DefaultPosition, wx.Size( 200,120 ), 0 )
		gSizer2.Add( self.m_buttonAec, 0, wx.ALL, 5 )


		bSizer2.Add( gSizer2, 1, wx.EXPAND, 5 )

		self.m_textCtrlInfo = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 800,150 ), 0 )
		self.m_textCtrlInfo.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "宋体" ) )

		bSizer2.Add( self.m_textCtrlInfo, 0, wx.ALL, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		self.m_toolBar1.Realize()


		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.OnMenuExit, id = self.m_menuItemExit.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuAbout, id = self.m_menuItemAbout.GetId() )
		self.m_buttonTestAll.Bind( wx.EVT_BUTTON, self.OnButtonTestAll )
		self.m_buttonLeftMic.Bind( wx.EVT_BUTTON, self.OnButtonLeftMic )
		self.m_buttonRightMic.Bind( wx.EVT_BUTTON, self.OnButtonRightMic )
		self.m_buttonRef.Bind( wx.EVT_BUTTON, self.OnButtonRef )
		self.m_buttonAec.Bind( wx.EVT_BUTTON, self.OnButtonAec )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnMenuExit( self, event ):
		event.Skip()

	def OnMenuAbout( self, event ):
		event.Skip()

	def OnButtonTestAll( self, event ):
		event.Skip()

	def OnButtonLeftMic( self, event ):
		event.Skip()

	def OnButtonRightMic( self, event ):
		event.Skip()

	def OnButtonRef( self, event ):
		event.Skip()

	def OnButtonAec( self, event ):
		event.Skip()


###########################################################################
## Class DialogAbout
###########################################################################

class DialogAbout ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"关于", pos = wx.DefaultPosition, size = wx.Size( 400,150 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"版本：V1.0\n作者：熊汉良", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer3.Add( self.m_staticText1, 0, wx.ALL, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


