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
        self.mainText.Bind(wx.EVT_TEXT, self.onMainTextInput)

    #########################
    def onMainTextInput(self, event):
        self.record_data.save_record(event.String)

    #########################
    def showAppendMainText(self, text):
        old_text = self.mainText.GetValue()
        self.showMainText(old_text + u'\n' + text)

    def showAppendInfo(self, text):
        old_text = self.infoText.GetValue()
        self.showInfo(old_text + u'\n' + text)

    def showMainText(self, text):
        if not text:
            return
        try:
            self.mainText.SetValue(text)
        except Exception, e:
            self.showInfo(str(e))

    def showInfo(self, text):
        if not text:
            return
        try:
            self.infoText.SetValue(text)
        except Exception, e:
            self.infoText.SetValue(str(e))

    def showStatus(self, text):
        self.statusBar.SetStatusText(text, 0)

    #########################
    def cleanMainText(self):
        self.mainText.SetValue('')

    #########################
    # def onFileOpenButtonClick(self, evt):
    #     dlg = wx.FileDialog(self, u'选择要批处理的文件',
    #                         style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
    #                         )
    #     if dlg.ShowModal() == wx.ID_OK:
    #         self.folderPath = None
    #         self.files = dlg.GetPaths()
    #         self.openFiles(self.files)
    #     dlg.Destroy()

    # def openFiles(self, files):
    #     if not files:
    #         return
    #     for file_path in files:
    #         self.openFile(file_path)
    #     self.showInfo(u'\n'.join(files))
    #     self.showStatus(u'File open succeed.')

    # def openFile(self, file_path):
    #     with open(file_path, 'r') as f:
    #         text = f.read()
    #         self.sourceFiles.append({'file_path': file_path, 'text': text})

    #########################
    # def search(self):
    #     key = self.buttonBox.getSearchKey()
    #     self.cleanMainText()
    #     self.showInfo('Search key: ' + key)
    #     result_list = self.search_file_list(key, self.sourceFiles)
    #     self.print_result_list(result_list)
    #     self.showStatus('Search finished.')

    # def search_file_list(self, key, file_list):
    #     result_list = []
    #     for file_item in self.sourceFiles:
    #         file_path = file_item['file_path']
    #         self.showAppendInfo(file_path)
    #         result, s = self.search_file(key, file_item)
    #         if result:
    #             result_list.append({'s': s, 'result': result, 'file_path': file_path})
    #     return result_list


    # def search_file(self, key, file_item):
    #     return search.search(file_item['text'], key)

    # def print_result_list(self, result_list):
    #     result_list.sort(key=lambda x: x['s'], reverse=True)
    #     for item in result_list:
    #         self.show_result(item['file_path'], item['result'])

    def show_result(self, file_path, result):
        self.showAppendMainText(file_path)
        result_output = search.result_str(result)
        self.showAppendMainText(result_output)


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
