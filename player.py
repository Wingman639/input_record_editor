# -*- coding:UTF-8 -*-
import wx
import time
import buttonPanel


START_TIMESTAMP = time.time()


class ClientFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, -1, u'Input Record Replay', size=(1000, 800)
            )
        self.sourceFiles = []
        self.file_path = None
        self.latest_timestamp = None
        self.folderPath = ''
        self.lastOpenFolderPath = ''
        self.lastSaveFolderPath = ''
        self.addStatusBar()
        self.splitWindow = wx.SplitterWindow(self)
        self.mainPanel = self.newMainPanel(self.splitWindow)
        self.infoPanel = self.newInfoPanel(self.splitWindow)
        self.splitWindow.SplitHorizontally(self.mainPanel, self.infoPanel, -100)
        self.splitWindow.SetMinimumPaneSize(20)
        self.bindEvents()


    def newMainPanel(self, parent):
        mainPanel = wx.Panel(parent, -1)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.buttonBox = buttonPanel.ButtonBox(mainPanel)
        mainSizer.Add(self.buttonBox, proportion=0, flag= wx.TOP, border=5)

        self.mainText = wx.TextCtrl(mainPanel, -1, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
        mainSizer.Add(self.mainText, proportion= 1, flag=wx.TOP | wx.EXPAND, border=5)
        #self.grid = grid.FileTableGrid(mainPanel)
        #mainSizer.Add(self.grid, proportion= 1, flag=wx.TOP | wx.EXPAND,  border=5)

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
        self.buttonBox.buttonOpenFile.Bind(wx.EVT_BUTTON,
                                           self.onFileOpenButtonClick)
        self.buttonBox.buttonPlay.Bind(wx.EVT_BUTTON,
                                         self.onFileOpenPlayClick)
        #self.mainText.Bind(wx.EVT_TEXT, self.onMainTextChange)

    #########################
    def onFileOpenButtonClick(self, evt):
        wildcard = "Data files (*.data)|*.data|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, u'open recording file',
                            wildcard=wildcard,
                            style=wx.OPEN | wx.CHANGE_DIR
                            )
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = None
            self.file_path = dlg.GetPath()
            self.showAppendInfo(self.file_path)
            #self.openFile(self.file_path)
        dlg.Destroy()

    def onFileOpenPlayClick(self, evt):
        self.replay(self.file_path)


    def onMainTextChange(self, event):
        self.reply_one_step()

    #########################

    def replay(self, file_path):
        text = self.read_file(file_path)
        #self.lines = text.splitlines()
        #start_line = self.lines[0]
        lines = text.splitlines()
        start_line = lines[0]
        self.init_start_time(start_line)
        self.line_index = 0
        #self.replay_one_step()
        records_lines = lines[1:-1]
        self.replay_records(records_lines)
        end_line = lines[-1]
        self.showAppendInfo('\n' + end_line)


    def replay_records(self, records_lines):
        for line in records_lines:
            self.show_one_step(line)


    def init_start_time(self, line):
        start = eval(line)
        self.latest_timestamp = start[1]


    def show_one_step(self, line):
        record = eval(line)
        if self.latest_timestamp:
            timestamp = record[1]
            interval = timestamp - self.latest_timestamp
            self.latest_timestamp = timestamp
            self.showAppendInfo('\n' + line + ' ' + str(interval))
            time.sleep(interval)
        self.showMainText(record[0])


    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            return f.read()

    def replay_one_step(self):
        self.line_index += 1
        line = self.lines[self.line_index]
        self.show_one_step(line)

    #########################
    def showAppendMainText(self, text):
        if not text:
            return
        try:
            self.mainText.AppendText(text)
        except Exception, e:
            self.showInfo(str(e))

    def showAppendInfo(self, text):
        if not text:
            return
        try:
            self.infoText.AppendText(text)
        except Exception, e:
            self.infoText.AppendText(str(e))

    def showMainText(self, text):
        if not text:
            return
        try:
            self.mainText.Value = text
            self.mainText.Update()
        except Exception, e:
            self.showInfo(str(e))

    def showInfo(self, text):
        if not text:
            return
        try:
            self.infoText.SetValue(text)
            self.infoText.Update()
        except Exception, e:
            self.infoText.SetValue(str(e))
            self.infoText.Update()

    def showStatus(self, text):
        self.statusBar.SetStatusText(text, 0)

    #########################
    def cleanMainText(self):
        self.mainText.Value = ''
        self.mainText.Update()

    #########################
    def show_result(self, file_path, result):
        self.showAppendMainText(file_path)
        result_output = search.result_str(result)
        self.showAppendMainText(result_output)


def run_window():
    app = wx.PySimpleApp()
    frame = ClientFrame()
    frame.Show(True)
    app.MainLoop()

def main():
    run_window()

if __name__ == '__main__':
    main()
