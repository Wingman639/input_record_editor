# -*- coding:UTF-8 -*-
import wx
import os
import time
import codecs
from record_data import InputRecord
import os_cmd

START_TIMESTAMP = time.time()
CTRL_EFFECT_TIME = 0.2


class ClientFrame(wx.Frame):
    def __init__(self, record_data):
        wx.Frame.__init__(
            self, None, -1, u'Editor', size=(1000, 600)
            )
        self.ctrl_time = 0
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

        self.mainText = wx.TextCtrl(mainPanel, -1, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER)
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
        self.mainText.Bind(wx.EVT_KEY_DOWN, self.onMainTextKeyDown)

    #########################
    def onMainTextInput(self, event):
        self.record_data.save_record(event.String)

    def onMainTextKeyDown(self, event):
        if event.CmdDown():
            self.ctrl_time = time.time()
        if event.GetKeyCode() == ord('B') and self.ctrl_time:
            if time.time() - self.ctrl_time < CTRL_EFFECT_TIME:
                # self.infoText.AppendText('Ctrl+B: Building...')
                self.build()
        event.Skip(True)




    #########################
    def build(self):
        self.infoTextClean()
        code_path = self.save()
        cmd = ['python', code_path]
        # print cmd
        start_time = time.time()
        output = os_cmd.check_output(cmd)
        end_time = time.time()
        self.infoText.AppendText(output + '\n')
        self.infoText.AppendText('[Finished in %.2f]' % (end_time - start_time))


    def save(self):
        # code_path = self._generate_file_path()
        code_path = 'code.py'
        text = self.mainText.GetValue()
        text = self.replace_to_ascii_punctuation(text)
        with codecs.open(code_path, 'w', 'utf-8') as file:
            file.write(text)
        return code_path

    def replace_to_ascii_punctuation(self, text):
        known_punctuation = {u'‘': '\'',
                             u'’': '\'',
                             u'“': '"',
                             u'”': '"',
                            }
        for key, value in known_punctuation.items():
            text = text.replace(key, value)
        return text

    def infoTextClean(self):
        self.infoText.SetValue('')
        self.infoText.Update()


    # def _generate_file_path(self):
    #     return os.path.join(
    #                 os.path.dirname(os.path.abspath('__file__')),
    #                 'code.py')


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
