#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.5 on Sat Sep 15 14:23:13 2007 from D:\Users\Maarten\Projects\Gimias\Prog\GIMIAS.cmake\GBuild\csnGUI.wxg

import wx
from wx import xrc
import csnGUIHandler
import csnGUIOptions
import csnContext
import csnContextConverter
import csnBuild
import csnUtility
import os.path
import sys
import shutil
import time
import subprocess
import xrcbinder
from optparse import OptionParser

class RedirectText:
    """
    Used to redirect messages to stdout to the text control in CSnakeGUIFrame.
    """
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
        self.out.Update()

class SelectFolderCallback:
    """ 
    Lets the user choose a path, then calls 'callback' to set the path value in the domain layer, 
    and calls app.UpdateGUIAndSaveContextAndOptions.
    """
    def __init__(self, message, callbackGet, callbackSet, app):
        self.message = message
        self.callbackGet = callbackGet
        self.callbackSet = callbackSet
        self.app = app
        
    def __call__(self, event = None):
        oldValue = self.callbackGet()
        
        dlg = wx.DirDialog(None, self.message, oldValue, wx.DD_DIR_MUST_EXIST)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.callbackSet(dlg.GetPath().replace("\\", "/"))
        self.app.UpdateGUIAndSaveContextAndOptions()
        
class CSnakeGUIApp(wx.App):
    def OnInit(self):
        self.destroyed = False
        self.listOfPossibleTargets = []
        self.projectCheckBoxes = dict()
        
        wx.InitAllImageHandlers()
        xrcFile = csnUtility.GetRootOfCSnake() + "/resources/csnGUI.xrc"
        self.res = xrc.XmlResource(xrcFile)
        self.InitFrame()
        self.InitMenu()
        self.InitOtherGUIStuff()		
        self.Initialize()
        self.SetTopWindow(self.frame)
        return 1

    def InitFrame(self):
        self.frame = self.res.LoadFrame(None, "frmCSnakeGUI")
        self.binder = xrcbinder.Binder(self, self.frame)
        
        self.textLog = xrc.XRCCTRL(self.frame, "textLog")
        self.binder.AddTextControl("txtBuildFolder", buddyClass = "context", buddyField = "buildFolder", isFilename = True)
        self.binder.AddTextControl("txtThirdPartyBuildFolder", buddyClass = "context", buddyField = "thirdPartyBuildFolder", isFilename = True)
        self.binder.AddTextControl("txtInstallFolder", buddyClass = "context", buddyField = "installFolder", isFilename = True)
        self.binder.AddTextControl("txtKDevelopProjectFolder", buddyClass = "context", buddyField = "kdevelopProjectFolder", isFilename = True)
        self.binder.AddTextControl("txtThirdPartyRootFolder", buddyClass = "context", buddyField = "thirdPartyRootFolder", isFilename = True)
        self.binder.AddTextControl("txtCMakePath", buddyClass = "context", buddyField = "cmakePath", isFilename = True)
        self.binder.AddTextControl("txtPythonPath", buddyClass = "context", buddyField = "pythonPath", isFilename = True)
        self.binder.AddTextControl("txtVisualStudioPath", buddyClass = "context", buddyField = "idePath", isFilename = True)
        self.binder.AddComboBox("cmbCSnakeFile", valueListFunctor = self.GetCSnakeFileComboBoxItems, buddyClass = "context", buddyField = "csnakeFile", isFilename = True)
        self.binder.AddComboBox("cmbInstance", valueListFunctor = self.GetInstanceComboBoxItems, buddyClass = "context", buddyField = "instance")
        self.binder.AddComboBox("cmbCompiler", valueListFunctor = self.GetCompilerComboBoxItems, buddyClass = "context", buddyField = "compiler")
        self.binder.AddComboBox("cmbBuildType", valueListFunctor = self.GetBuildTypeComboBoxItems, buddyClass = "context", buddyField = "configurationName")
        self.binder.AddListBox("lbRootFolders", buddyClass = "context", buddyField = "rootFolders", isFilename = True)
        self.binder.AddCheckBox("chkAskToLaunchVisualStudio", buddyClass = "options", buddyField = "askToLaunchIDE")
        
        self.panelKDevelop = xrc.XRCCTRL(self.frame, "panelKDevelop")
        self.noteBook = xrc.XRCCTRL(self.frame, "noteBook")
        self.noteBook.SetSelection(0)
        
        self.panelSelectProjects = xrc.XRCCTRL(self.frame, "panelSelectProjects")
        self.statusBar = xrc.XRCCTRL(self.frame, "statusBar")

<<<<<<< .mine
        self.panelContext = xrc.XRCCTRL(self.frame, "panelContext")

        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Binary Folder", self.SetBuildFolder, self), id=xrc.XRCID("btnSelectBuildFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Install Folder", self.SetInstallFolder, self), id=xrc.XRCID("btnSelectInstallFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Third Party Root Folder", self.SetThirdPartyRootFolder, self), id=xrc.XRCID("btnSelectThirdPartyRootFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Third Party Bin Folder", self.SetThirdPartyBuildFolder, self), id=xrc.XRCID("btnSelectThirdPartyBuildFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select folder for saving the KDevelop project file", self.SetKDevelopProjectFolder, self), id=xrc.XRCID("btnSelectKDevelopProjectFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Add root folder", self.AddRootFolder, self), id=xrc.XRCID("btnAddRootFolder"))
=======
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Binary Folder", self.GetBuildFolder, self.SetBuildFolder, self), id=xrc.XRCID("btnSelectBuildFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Install Folder", self.GetInstallFolder, self.SetInstallFolder, self), id=xrc.XRCID("btnSelectInstallFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Third Party Root Folder", self.GetThirdPartyRootFolder, self.SetThirdPartyRootFolder, self), id=xrc.XRCID("btnSelectThirdPartyRootFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select Third Party Bin Folder", self.GetThirdPartyBuildFolder, self.SetThirdPartyBuildFolder, self), id=xrc.XRCID("btnSelectThirdPartyBuildFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Select folder for saving the KDevelop project file", self.GetKDevelopProjectFolder, self.SetKDevelopProjectFolder, self), id=xrc.XRCID("btnSelectKDevelopProjectFolder"))
        self.frame.Bind(wx.EVT_BUTTON, SelectFolderCallback("Add root folder", self.GetLastRootFolder, self.AddRootFolder, self), id=xrc.XRCID("btnAddRootFolder"))
>>>>>>> .r388
        self.frame.Bind(wx.EVT_BUTTON, self.OnDetectRootFolders, id=xrc.XRCID("btnDetectRootFolders"))

        self.frame.Bind(wx.EVT_BUTTON, self.OnSetCMakePath, id=xrc.XRCID("btnSetCMakePath"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnSetPythonPath, id=xrc.XRCID("btnSetPythonPath"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnSelectCSnakeFile, id=xrc.XRCID("btnSelectCSnakeFile"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnSetVisualStudioPath, id=xrc.XRCID("btnSetVisualStudioPath"))

        self.frame.Bind(wx.EVT_BUTTON, self.RefreshProjects, id=xrc.XRCID("btnForceRefreshProjects"))
        self.btnForceRefreshProjects = xrc.XRCCTRL(self.frame, "btnForceRefreshProjects")
        
        self.frame.Bind(wx.EVT_BUTTON, self.OnRemoveRootFolder, id=xrc.XRCID("btnRemoveRootFolder"))
        self.frame.Bind(wx.EVT_COMBOBOX, self.OnSelectRecentlyUsed, id=xrc.XRCID("cmbCSnakeFile"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnUpdateListOfTargets, id=xrc.XRCID("btnUpdateListOfTargets"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnCreateCMakeFilesAndRunCMake, id=xrc.XRCID("btnCreateCMakeFilesAndRunCMake"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnOnlyCreateCMakeFiles, id=xrc.XRCID("btnOnlyCreateCMakeFiles"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnConfigureThirdPartyFolder, id=xrc.XRCID("btnConfigureThirdPartyFolder"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnInstallFilesToBuildFolder, id=xrc.XRCID("btnInstallFilesToBuildFolder"))
        self.frame.Bind(wx.EVT_BUTTON, self.OnLaunchIDE, id=xrc.XRCID("btnLaunchIDE"))
        self.frame.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNoteBookPageChanged, id=xrc.XRCID("noteBook"))
        
    def OnNoteBookPageChanged(self, event):
        if self.noteBook.GetPageText(self.noteBook.GetSelection()) == "Select Projects":
            self.SelectProjects()
        
    def InitMenu(self):
        self.frame.Bind(wx.EVT_MENU, self.OnContextOpen, id=xrc.XRCID("mnuContextOpen"))
        self.frame.Bind(wx.EVT_MENU, self.OnContextCreateACopy, id=xrc.XRCID("mnuContextCreateACopy"))
        self.frame.Bind(wx.EVT_MENU, self.OnContextAbandonChanges, id=xrc.XRCID("mnuContextAbandonChanges"))
        self.frame.Bind(wx.EVT_MENU, self.OnExit, id=xrc.XRCID("mnuExit"))
        
    def InitOtherGUIStuff(self):
        # connect close event
        self.frame.Bind(wx.EVT_CLOSE, self.OnExit, self.frame)
        
        #self.frame.GetSizer().Remove(xrc.XRCID(self.frame, "boxInstallFolder"))
        self.frame.Show()		
        
    def Initialize(self):
        """
        Initializes the application.
        """
        self.LoadIcon()
        self.ParseCommandLine()
        if not self.commandLineOptions.console:
            self.RedirectStdOut()
        self.PrintWelcomeMessages()
        self.CreateHandler()
        self.InitializeOptions()    
        
        # load previously saved context
        contextToLoad = self.options.contextFilename
        if len(self.commandLineArgs) >= 1:
            contextToLoad = self.commandLineArgs[0]
            
        if self.LoadContext(contextToLoad):
            self.BackupContextFile()

        self.UpdateGUIAndSaveContextAndOptions()
        
    def Warn(self, message):
        if message is None:
            return
        """ Shows a warning message to the user. ToDo: do some more fancy than print."""
        print message + "\n"
        
    def Error(self, message):
        """ Shows an error message to the user. ToDo: do some more fancy than print."""
        if message is None:
            return
        print message + "\n"

    def Report(self, message):
        if message is None:
            return
        print message + "\n"

    def BackupContextFile(self):
        """ Creates a backup of the current context, so that the user can later abandon all his changes. """
        self.contextBeforeEditingFilename = "%s/contextBeforeEditing" % self.thisFolder
        try:
            shutil.copy(self.options.contextFilename, self.contextBeforeEditingFilename)
        except:
            message = "Warning: could not copy %s to backup location %s" % (self.options.contextFilename, self.contextBeforeEditingFilename)
            self.Warn(message)

    def SetStatus(self, message):
        self.statusBar.SetFields([message])
        
    def LoadIcon(self):
        iconFile = csnUtility.GetRootOfCSnake() + "/resources/Laticauda_colubrina.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(icon1)
    
    def ParseCommandLine(self):
        parser = OptionParser()
        parser.add_option("-c", "--console", dest="console", default=False, help="print all messages to the console window")
        (self.commandLineOptions, self.commandLineArgs) = parser.parse_args()
        self.thisFolder = "%s" % (os.path.dirname(sys.argv[0]))
        self.thisFolder = self.thisFolder.replace("\\", "/")
        if self.thisFolder == "":
            self.thisFolder = "."
    
    def RedirectStdOut(self):
        # redirect std out
        self.redir=RedirectText(self.textLog)
        sys.stdout=self.redir
        sys.stderr=self.redir

    def PrintWelcomeMessages(self):
        self.Report("CSnake version = %s\n" % csnBuild.version)

    def CreateHandler(self):
        self.handler = csnGUIHandler.Handler()
        self.context = None
    
    def InitializeOptions(self):
        self.options = csnGUIOptions.Options()
        self.binder.SetBuddyClass("options", self.options)

        self.optionsFilename = "%s/options" % self.thisFolder
        self.converter = csnContextConverter.Converter(self.optionsFilename)
        
        if os.path.exists(self.optionsFilename):
            self.converter.ConvertOptions()
            self.options.Load(self.optionsFilename)
        else:
            self.options.contextFilename = "%s/default.csnakecontext" % self.thisFolder
            self.options.Save(self.optionsFilename)
            
        if not os.path.exists(self.options.contextFilename):
            self.options.contextFilename = "%s/context" % self.thisFolder
            csnContext.Context().Save(self.options.contextFilename)
        
    def CopyGUIToContextAndOptions(self):
        """ Copy all GUI fields to the current context """
        self.binder.UpdateBuddies()
        
    def SaveContextAndOptions(self, contextFilename = ""):
        """
        Copy context from the widget controls to self.context.
        If filename is not "", save current configuration context (source folder/build folder/etc) 
        to filename.
        """
        self.CopyGUIToContextAndOptions()
        if not contextFilename == "":
            self.options.contextFilename = contextFilename
        try:
            self.context.Save(self.options.contextFilename)
            self.frame.SetTitle("CSnake GUI - %s" % self.options.contextFilename)
        except:
            self.Error("Sorry, CSnakeGUI could not save the context to %s\n. Please check if another program is locking this file.\n" % self.options.contextFilename)
            
        try:
            self.options.Save(self.optionsFilename)
        except:
            self.Error("Sorry, CSnakeGUI could not save the options to %s\n. Please check if another program is locking this file.\n" % self.optionsFilename)
    
    def OnCreateCMakeFilesAndRunCMake(self, event):
        self.action = self.ActionCreateCMakeFilesAndRunCMake
        self.DoAction()
        
    def OnDetectRootFolders(self, event):
        additionalRootFolders = self.handler.FindAdditionalRootFolders()
        self.context.rootFolders.extend(additionalRootFolders)
        self.UpdateGUIAndSaveContextAndOptions()
    
    def FindAdditionalRootFolders(self, onlyForNewInstance=False):
        if onlyForNewInstance and self.context.IsCSnakeFileInRecentlyUsed():
            return
        
        additionalRootFolders = self.handler.FindAdditionalRootFolders()
        if len(additionalRootFolders):
            message =  "CSnakeGUI found additional root folders which are likely to be necessary for target %s.\n" % self.context.instance
            message += "Should CSnakeGUI add the following root folders?\n\n"
            for folder in additionalRootFolders:
                message += folder + "\n"
            message += "\n\nThis question will not appear again for this target, but you can later add the above root folders\nusing the Detect button\n"
                
            dlg = wx.MessageDialog(self.frame, message, style = wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                self.context.rootFolders.extend(additionalRootFolders)
                self.UpdateGUIAndSaveContextAndOptions()
            
    def ActionCreateCMakeFilesAndRunCMake(self):
        self.FindAdditionalRootFolders(True)
        if self.handler.ConfigureProjectToBuildFolder(_alsoRunCMake = True, _callback = self):
            xrc.XRCCTRL(self.panelContext, "btnLaunchIDE").SetFocus()
            xrc.XRCCTRL(self.panelContext, "btnOnlyCreateCMakeFiles").Disable()            
            xrc.XRCCTRL(self.panelContext, "btnCreateCMakeFilesAndRunCMake").Disable()
            if self.context.instance.lower() == "gimias":
                self.ProposeToDeletePluginDlls(self.handler.GetListOfSpuriousPluginDlls(_reuseInstance = True))
        
    def OnOnlyCreateCMakeFiles(self, event):
        self.action = self.ActionOnlyCreateCMakeFiles
        self.DoAction()
        
    def ActionOnlyCreateCMakeFiles(self):
        self.FindAdditionalRootFolders(True)
        if self.handler.ConfigureProjectToBuildFolder(_alsoRunCMake = False):
            if self.context.instance.lower() == "gimias":
                self.ProposeToDeletePluginDlls(self.handler.GetListOfSpuriousPluginDlls(_reuseInstance = True))
        
    def OnConfigureThirdPartyFolder(self, event):
        self.action = self.ActionConfigureThirdPartyFolder
        self.DoAction()
        
    def ActionConfigureThirdPartyFolder(self):
        if self.handler.ConfigureThirdPartyFolder():
            xrc.XRCCTRL(self.panelContext, "btnInstallFilesToBuildFolder").SetFocus()
            xrc.XRCCTRL(self.panelContext, "btnConfigureThirdPartyFolder").Disable()

            if self.options.askToLaunchIDE:
                self.AskToLaunchIDE( self.handler.GetThirdPartySolutionPath() )
        
    def OnInstallFilesToBuildFolder(self, event):
        self.action = self.ActionInstallFilesToBuildFolder
        self.DoAction()

        
    def ActionInstallFilesToBuildFolder(self):
        self.FindAdditionalRootFolders(True)
        if not self.handler.InstallBinariesToBuildFolder():
            self.Error("Error while installing files.")
        else:
            xrc.XRCCTRL(self.panelContext, "btnCreateCMakeFilesAndRunCMake").SetFocus()
            xrc.XRCCTRL(self.panelContext, "btnInstallFilesToBuildFolder").Disable()

            
    def DoAction(self):
        self.SetStatus("Processing...")
        self.textLog.Clear()
        self.textLog.Refresh()
        self.textLog.Update()
        
        self.Report("--- Working, patience please... ---")
        self.SaveContextAndOptions()
        startTime = time.time()
        
        try:
            self.action()
        except AssertionError, e:
            self.Error(str(e))
            
        elapsedTime = time.time() - startTime
        self.Report("--- Done (%d seconds) ---" % elapsedTime)
        self.UpdateGUIAndSaveContextAndOptions()
        self.SetStatus("")
        
        #self.Restart()
        
    def Restart(self):
        """ Restart the application """
        arglist = []
        if( os.path.splitext(os.path.basename(sys.executable))[0].lower() == "python" ):
            arglist = [sys.executable]
            arglist.extend(sys.argv)
        os.execv(sys.executable, arglist)
                
    def OnSelectCSnakeFile(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        """
        Select file containing the project that should be configured.
        """
        # Set path of that file that was selected before
        oldValue = self.context.csnakeFile
        if oldValue == "":
            oldPath = ""
        else:
            oldPathAndFilenameSplit = oldValue.rsplit("/", 1)
            oldPath = oldPathAndFilenameSplit[0] + "/"
        
        dlg = wx.FileDialog(None, "Select CSnake file", wildcard = "Python source files (*.py)|*.py", defaultDir = oldPath, defaultFile = oldValue)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.context.csnakeFile = dlg.GetPath()
            self.UpdateGUIAndSaveContextAndOptions()

    def SetBuildFolder(self, folder):
        self.context.buildFolder = folder
        
    def GetBuildFolder(self):
        return self.context.buildFolder
        
    def SetInstallFolder(self, folder):
        self.context.installFolder = folder

    def GetInstallFolder(self):
        return self.context.installFolder
        
    def SetThirdPartyRootFolder(self, folder):
        self.context.thirdPartyRootFolder = folder
    
    def GetThirdPartyRootFolder(self):
        return self.context.thirdPartyRootFolder
        
    def SetThirdPartyBuildFolder(self, folder):
        self.context.thirdPartyBuildFolder = folder
        
    def GetThirdPartyBuildFolder(self):
        return self.context.thirdPartyBuildFolder
        
    def SetKDevelopProjectFolder(self, folder):
        self.context.kdevelopProjectFolder = folder
        
    def GetKDevelopProjectFolder(self):
        return self.context.kdevelopProjectFolder
            
    def AddRootFolder(self, folder): # wxGlade: CSnakeGUIFrame.<event_handler>
        """
        Add folder where CSnake files must be searched to context.rootFolders.
        """
        self.context.rootFolders.append(folder)
    
    def GetLastRootFolder(self):
        if len(self.context.rootFolders) > 0:
            return self.context.rootFolders[len(self.context.rootFolders)-1]
        else:
            return ""

    def OnRemoveRootFolder(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        """
        Remove folder where CSnake files must be searched from context.rootFolders.
        """
        self.context.rootFolders.remove(self.lbRootFolders.GetStringSelection())
        self.UpdateGUIAndSaveContextAndOptions()

    def OnContextOpen(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        """
        Let the user load a context.
        """
        dlg = wx.FileDialog(None, "Select CSnake context file", wildcard = "Context Files (*.CSnakeGUI;*.csnakecontext)|*.CSnakeGUI;*.csnakecontext|All Files (*.*)|*.*")
        if dlg.ShowModal() == wx.ID_OK:
            if self.LoadContext(dlg.GetPath()):
                self.BackupContextFile()

    def OnContextCreateACopy(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        """
        Let the user save the context.
        """
        dlg = wx.FileDialog(None, "Copy CSnake context to...", wildcard = "*.CSnakeGUI", style = wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            (root, ext) = os.path.splitext(dlg.GetPath())
            if ext == ".CSnakeGUI":
                contextFilename = dlg.GetPath()
            else:
                contextFilename = "%s.CSnakeGUI" % root
            contextFilename = dlg.GetPath()
            self.SaveContextAndOptions(contextFilename)

    def GetCompilerComboBoxItems(self):
        result = []
        result.append("Visual Studio 7 .NET 2003")
        result.append("Visual Studio 8 2005")
        result.append("Visual Studio 8 2005 Win64")
        result.append("Visual Studio 9 2008")
        result.append("Visual Studio 9 2008 Win64")
        result.append("KDevelop3")
        result.append("Unix Makefiles")        
        return result
        
    def GetBuildTypeComboBoxItems(self):
        result = []
        result.append("DebugAndRelease")
        result.append("Release")
        result.append("Debug")
        return result
    
    def GetCSnakeFileComboBoxItems(self):
        result = list()
        count = 0
        for x in self.context.recentlyUsed:
            result.append("%s - In %s" % (x.instance, x.csnakeFile))
            count += 1
            if count >= 10:
                break
        return result
    
    def UpdateGUIAndSaveContextAndOptions(self):
        """ Refreshes the GUI based on the current context. Also saves the current context to the contextFilename """
        self.binder.UpdateControls()
        self.panelKDevelop.Show( self.context.compiler in ("KDevelop3", "Unix Makefiles") )
        self.SaveContextAndOptions()
        self.frame.Layout()
        self.frame.Refresh()
        self.frame.Update()
        wx.CallAfter(self.frame.Update)
    
    def LoadContext(self, contextFilename = ""):
        """
        Load configuration context from contextFilename.
        """
            
        if contextFilename == "":
            contextFilename = self.options.contextFilename
        else:
            self.options.contextFilename = contextFilename
            
        if not os.path.exists(self.options.contextFilename):
            self.Error("CSnakeGUI could not find context file %s" % self.options.contextFilename)
            return False
        
        try:
            if not self.converter.Convert(self.options.contextFilename):
                self.Error("CSnakeGUI tried to open %s, but this file is not a valid context file" % self.options.contextFilename)
                return False
            self.SetContext(self.handler.LoadContext(contextFilename))
            self.frame.SetTitle("CSnake GUI - %s" % self.options.contextFilename)
            self.UpdateGUIAndSaveContextAndOptions()
        except:
            self.Error("CSnakeGUI tried to open %s, but this file is not a valid context file" % self.options.contextFilename)
            return False

        return True

    def SetContext(self, context):
        self.context = context
        self.binder.SetBuddyClass("context", self.context)
        
    def OnUpdateListOfTargets(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        self.SetStatus("Retrieving list of targets")
        self.listOfPossibleTargets = self.handler.GetListOfPossibleTargets()
        if len(self.listOfPossibleTargets):
            self.context.instance = self.listOfPossibleTargets[0]
        self.UpdateGUIAndSaveContextAndOptions()
        self.SetStatus("")
        xrc.XRCCTRL(self.panelContext, "btnOnlyCreateCMakeFiles").Enable()
        xrc.XRCCTRL(self.panelContext, "btnCreateCMakeFilesAndRunCMake").Enable()
        xrc.XRCCTRL(self.panelContext, "btnInstallFilesToBuildFolder").Enable()  
        xrc.XRCCTRL(self.panelContext, "btnConfigureThirdPartyFolder").Enable()


    def GetInstanceComboBoxItems(self):
        return self.listOfPossibleTargets
            
    def ProposeToDeletePluginDlls(self, spuriousDlls):
        if len(spuriousDlls) == 0:
            return
            
        dllMessage = ""
        for x in spuriousDlls:
            dllMessage += ("%s\n" % x)
            
        message = "In the build results folder, CSnake found GIMIAS plugins that have not been configured.\nThe following plugin dlls may crash GIMIAS:\n\n%s\nDelete them?" % dllMessage
        dlg = wx.MessageDialog(self.frame, message, style = wx.YES_NO)
        if dlg.ShowModal() != wx.ID_YES:
            return
            
        for dll in spuriousDlls:
            os.remove(dll)

    def AskToLaunchIDE(self, pathToSolution):
        message = "Launch Visual Studio with solution %s?" % pathToSolution
        dlg = wx.MessageDialog(self.frame, message, style = wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            argList = [self.context.idePath, pathToSolution]
            subprocess.Popen(argList)

    def OnLaunchIDE(self, event = None):
        argList = [self.context.idePath, self.handler.GetTargetSolutionPath()]
        subprocess.Popen(argList)
    
    def OnExit(self, event = None):
        if not self.destroyed:
            self.destroyed = True
            self.CopyGUIToContextAndOptions()
            if os.path.exists(self.options.contextFilename):
                self.SaveContextAndOptions(self.options.contextFilename)
            self.frame.Destroy()

    def OnSelectRecentlyUsed(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        item = self.cmbCSnakeFile.GetSelection()
        context = self.context.recentlyUsed[item]
        self.context.csnakeFile = context.csnakeFile
        self.context.instance = context.instance
        self.UpdateGUIAndSaveContextAndOptions()

    def OnContextAbandonChanges(self, event): # wxGlade: CSnakeGUIFrame.<event_handler>
        try:
            shutil.copy(self.contextBeforeEditingFilename, self.options.contextFilename)
            self.LoadContext()
        except:
            self.Warn("Sorry, could not copy %s to %s. You can try copying the file manually" % (self.contextBeforeEditingFilename, self.options.contextFilename))

    def OnSetCMakePath(self, event): # wxGlade: CSnakeOptionsFrame.<event_handler>
        """
        Let the user select where CSnake is located.
        """
        dlg = wx.FileDialog(None, "Select path to CMake")
        if dlg.ShowModal() == wx.ID_OK:
            self.context.cmakePath = dlg.GetPath()
            self.UpdateGUIAndSaveContextAndOptions()

    def OnSetPythonPath(self, event): # wxGlade: CSnakeOptionsFrame.<event_handler>
        dlg = wx.FileDialog(None, "Select path to Python")
        if dlg.ShowModal() == wx.ID_OK:
            self.context.pythonPath = dlg.GetPath()
            self.UpdateGUIAndSaveContextAndOptions()

    def OnSetVisualStudioPath(self, event): # wxGlade: CSnakeOptionsFrame.<event_handler>
        dlg = wx.FileDialog(None, "Select path to Python")
        if dlg.ShowModal() == wx.ID_OK:
            self.context.idePath = dlg.GetPath()
            self.UpdateGUIAndSaveContextAndOptions()

    def SelectProjects(self, forceRefresh = False):
        # get list of ALL the categories on which the user can filter
        self.SetStatus("Retrieving projects...")
        previousFilter = self.context.filter 
        self.context.filter = list()
        try:
            categories = self.handler.GetCategories(forceRefresh)
        except:
            message = "Could not load project dependencies for instance %s from file %s." % (self.context.instance, self.context.csnakeFile)
            message = message + "\nPlease check the fields 'CSnake File' and 'Instance'"
            self.Error(message)
            return
            
        self.context.filter = previousFilter
        
        # create list of checkboxes for the categories
        self.panelSelectProjects.GetSizer().Clear()
        for category in self.projectCheckBoxes.keys():
            self.projectCheckBoxes[category].Destroy()
        self.projectCheckBoxes.clear()
        
        for category in sorted(categories):
            self.projectCheckBoxes[category] = wx.CheckBox(self.panelSelectProjects, -1, category)
            self.projectCheckBoxes[category].SetValue( not category in self.context.filter )
            self.panelSelectProjects.GetSizer().Add(self.projectCheckBoxes[category], 0, 0, 3)
            self.panelSelectProjects.Bind(wx.EVT_CHECKBOX, self.OnCategoryCheckBoxChanged, self.projectCheckBoxes[category])

        # create list of checkboxes for the 'super categories' (which are groups of normal categories, such as Tests)
        for super in self.context.subCategoriesOf.keys():
            value = True
            for sub in self.context.subCategoriesOf[super]:
                    value = value and (not sub in self.context.filter)
                    
            self.projectCheckBoxes[super] = wx.CheckBox(self.panelSelectProjects, -1, super)
            self.projectCheckBoxes[super].SetValue( value )
            self.panelSelectProjects.GetSizer().Insert(0, self.projectCheckBoxes[super], 0, 0, 3)
            self.panelSelectProjects.Bind(wx.EVT_CHECKBOX, self.OnSuperCategoryCheckBoxChanged, self.projectCheckBoxes[super])
            
        self.panelSelectProjects.GetSizer().Add(self.btnForceRefreshProjects, 0, 0, 3)
        self.panelSelectProjects.Layout()
        self.SetStatus("")
        
    def OnSuperCategoryCheckBoxChanged(self, event): # wxGlade: CSnakeOptionsFrame.<event_handler>
        """ 
        Respond to checking a supercategory (such as Tests or Demos). Results in (un)checking all subcategories in that
        supercategory.
        """
        for super in self.context.subCategoriesOf.keys():
            value = self.projectCheckBoxes[super].GetValue()
                    
            for cbName in self.projectCheckBoxes.keys():
                if cbName in self.context.subCategoriesOf[super]:
                    self.projectCheckBoxes[cbName].SetValue(value)
                    
        self.OnCategoryCheckBoxChanged(event)
        
    def OnCategoryCheckBoxChanged(self, event): # wxGlade: Dialog.<event_handler>
        """ 
        Updates the category filter, based on the current status of the checkbox for each category.
        """
        for category in self.projectCheckBoxes.keys():
            if category in self.context.filter:
                self.context.filter.remove(category)
            if not self.projectCheckBoxes[category].GetValue():
                self.context.filter.append(category)

    def RefreshProjects(self, event):
        self.SelectProjects(forceRefresh=True)
    
if __name__ == "__main__":
    app = CSnakeGUIApp(0)
    app.MainLoop()
