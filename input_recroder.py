# -*- coding:UTF-8 -*-
import wx
import time
from record_data import InputRecord

START_TIMESTAMP = time.time()


class ClientFrame(wx.Frame):
    def __init__(self, record_data):
        wx.Frame.__init__(
            self, None, -1, u'Editor', size=(1000, 600)
            )
        self.record_data = record_data
        self.sourceFiles = []
        self.files = []
        self.folderPath = ''
        self.lastOpenFolderPath = ''
        self.lastSaveFolderPath = ''
        self.addStatusBar()
        self.splitWindow = wx.SplitterWindow(self)
        self.mainPanel = self.newMainPanel(self.splitWindow)
        self.infoPanel = self.newInfoPanel(self.splitWindow)
        self.splitWindow.SplitHorizontally(self.mainPanel, self.infoPanel, -200)
        self.splitWindow.SetMinimumPaneSize(20)
        self.bindEvents()


    def newMainPanel(self, parent):
        mainPanel = wx.Panel(parent, -1)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # self.buttonBox = buttonPanel.ButtonBox(mainPanel)
        # mainSizer.Add(self.buttonBox, proportion=0, flag= wx.TOP, border=5)

        self.mainText = wx.TextCtrl(mainPanel, -1, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
        mainSizer.Add(self.mainText, proportion= 1, flag=wx.TOP | wx.EXPAND, border=5)

        mainPanel.SetSizer(mainSizer)
        return mainPanel

    def newInfoPanel(self, parent):
        infoPanel = wx.Panel(parent)
        infoPanel.SetBackgroundColour("white")

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.infoText = wx.TextCtrl(infoPanel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.infoText, proportion=1, flag=wx.EXPAND | wx.ALL)
        infoPanel.SetSizerAndFit(vbox)
        return infoPanel

    def addStatusBar(self):
        self.statusBar = wx.StatusBar(self)
        self.SetStatusBar(self.statusBar)

    #########################
    def bindEvents(self):
        self.mainText.Bind(wx.EVT_TEXT, self.onMainTextInput)

    #########################
    def onMainTextInput(self, event):
        self.record_data.save_record(event.String)

    #########################




def run_window(record_data):
    app = wx.PySimpleApp()
    frame = ClientFrame(record_data)
    frame.Show(True)
    app.MainLoop()

def main():
    with InputRecord() as record_data:
        run_window(record_data)

if __name__ == '__main__':
    main()
