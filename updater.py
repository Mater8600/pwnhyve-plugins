# this will delete all of the plugins and replace them with newer versions #
from core.plugin import BasePwnhyvePlugin
from core.utils import *
from threading import Thread
from subprocess import getoutput
class PWNmaters(BasePwnhyvePlugin):
    def Update_Maters_Plugins(tpil):
        terminal = tpil.gui.screenConsole()
        terminal.addText("This module will update all of Mater's plugins for you :)\nPress any key to continue")
        tpil.waitForKey()
        try:
            getoutput("rm -r /root/pwnhyve/addons/plugins/Mater")
            getoutput("git clone https://github.com/Mater8600/pwnhyve-plugins.git /root/pwnhyve/addons/plugins/Mater")
            getoutput("rm -r /root/pwnhyve/addons/plugins/Mater/.git")
            getoutput("rm /root/pwnhyve/addons/plugins/Mater/README.md")
            getoutput("rm /root/pwnhyve/addons/plugins/Mater/updater.py")

        except:
            terminal.text = ""
            terminal.addText("Could not update are you connected to the internet?\nPress any key to exit")
            tpil.waitForKey()
            return
    #def Update_All_Plugins(tpil):
     #   terminal = tpil.gui.ScreenConsole()
      #  terminal.addText("This module will update all of the plugins in the plugins folder\nPress any button to continue\n(NOT FINISHED DOES NOTHING)")
       ##try:
          #  getoutput("rm -r /root/pwnhyve/addons/plugins/W")
