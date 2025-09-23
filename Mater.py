from core.plugin import BasePwnhyvePlugin
from core.utils import *
from threading import Thread
from subprocess import getoutput
import netifaces as ni
from scapy.all import ARP, Ether, srp, TCP, IP, sr
from pylaunch.dial import Dial
import time
import pychromecast
import zeroconf
import re
from pychromecast.controllers.youtube import YouTubeController
# Created by Mater #
class PWNmaters(BasePwnhyvePlugin):
    # This function is pretty good, needs more customization for ease of use #
    def hcxdumptool(tpil):
        """Capture handshakes using hcxdumptool"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("WARNING THIS TOOL SHOULD BE USED RESPONSIBLY\nUSE AT YOUR OWN RISK\nPress any key to continue...\n")
        tpil.waitForKey()
        tpil.clear()
        terminal.text = ""
        interface = "wlan1"
        terminal.addText(f"Using wireless interface: {interface}\n")

        # go into monitor mode #
        getoutput(f"sudo airmon-ng start {interface}")
        # I set it to the most common channels cause hopping takes forever -- reverted this because it causes issues rn using default#
        cmd = f"sudo hcxdumptool -i {interface}mon  -w /root/pwnhyve/handshakes/output.pcapng"
        terminal.addText("Press any key to stop\n")
        process = Thread(target=getoutput, args=(cmd,))
        process.start()
        tpil.waitForKey()
        terminal.text = ""
        getoutput("pkill hcxdumptool")
        process.join()
        terminal.addText("Capture stopped. Handshakes saved to /root/pwnhyve/handshakes\nPress any key to exit...")
        tpil.waitForKey()
        
        return
    
    
    def Convert_Handshakes(tpil):
        """Convert all handshakes in the handshake folder to a hashcat readable format"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("Converting all files in handshake folder")
        
        cmd = "sudo hcxpcapngtool /root/pwnhyve/handshakes/* -o /root/pwnhyve/handshakes/handshakes.22000"
        getoutput(cmd)
        terminal.addText("Wait a bit then press any key")
        tpil.waitForKey()
    # The port scanning is slow but it works, needs more work #
    def Discover_and_Scan(tpil):
        """Discover devices on the network using arp packets"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("This plugin will use arp packets to discover devices on the network\nPress any key to continue...\n")
        tpil.waitForKey()
        ### You have to sometimes hit the key twice or more because the arp scan returns non-scannable devices ###
        terminal.text = ""
        
        ip_address = ni.ifaddresses("wlan0")[ni.AF_INET][0]['addr']
        base_ip = '.'.join(ip_address.split('.')[:-1])
        tpil.clear()
        terminal.addText(f"Your IP address: {ip_address}\n")
        terminal.addText(f"Base IP: {base_ip}.0/24")
        terminal.addText(f"This may take a while, please wait...\n")
        terminal.text = ""
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.0.0/24"), timeout=2)
        common_ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,1521,3306,3389,5900,8080]
        for snd, rcv in ans:
            print(f"IP: {rcv.psrc} - MAC: {rcv.hwsrc}")
            try:
                res, unans = sr(IP(dst=rcv.psrc)/TCP(flags="S", dport=common_ports), timeout=2, verbose=0)
                open_ports = []
                for s, r in res:
                    if r.haslayer(TCP) and r[TCP].flags == 0x12:  
                        open_ports.append(s[TCP].dport)
                if open_ports:
                    print(f"Open ports on {rcv.psrc}: {open_ports}")
                    terminal.addText(f"{rcv.psrc} - Open ports: {open_ports}\n")

                tpil.waitForKey()
                terminal.text = ""
            except Exception as e:
                print(e)
                terminal.addText(f"Error scanning {rcv.psrc}\n")
                tpil.waitForKey()
                terminal.text = ""
        return
    # I am unable to kill the server properly, if you can find a fix let me know #
    def Share_Handshakes(tpil):
        """Share handshakes using a simple http server"""
        ip_address = ni.ifaddresses("wlan0")[ni.AF_INET][0]['addr']
        terminal = tpil.gui.screenConsole()
        terminal.addText(f"Starting a http server at {ip_address}:8888 to share handshakes\nPress any key to exit")
        
        cmd = "python3 -m http.server -d /root/pwnhyve/handshakes/ 8888"
        process = Thread(target=getoutput,args=(cmd,))
        process.start()
        
        tpil.waitForKey()

        getoutput("pkill http.server")
        
        return
    # I dont know if the dial protocol is working properly, open an issue if you can test this #
    # The chromecast part works fine and it even turns on tvs with chromecast in it! #
    def Cast(tpil):
        """Cast to all tvs on your network"""
        terminal =tpil.gui.screenConsole()
        terminal.addText("This module can cast to all tvs on your network\nUSE WITH CAUTION!\nPress any key to continue...")
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
        terminal.addText("Never gonna give you up has been sent to all tvs on your network\nPress any key to exit...")
        tpil.waitForKey()
        return
    def Delete_Pcap(tpil):
        """Delete all pcap files in the handshake folder"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("This will delete all pcap files in the handshake folder\nPress any key to continue...")
        tpil.waitForKey()
        getoutput("rm /root/pwnhyve/handshakes/output*")
        terminal.addText("All pcap files deleted\nPress any key to exit...")
        tpil.waitForKey()
        return
    def Delete_Hash(tpil):
        """Delete all hash files in the handshake folder"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("This will delete all hash files in the handshake folder\nPress any key to continue...")
        tpil.waitForKey()
        getoutput("rm /root/pwnhyve/handshakes/handshakes*")
        terminal.addText("All hash files deleted\nPress any key to exit...")
        tpil.waitForKey()
        return
    def About(tpil):
        """About Mater's utils"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("Mater's utils v1.3\nCreated by Mater8600\nThanks for downloading!\nPress any key to exit...")
        tpil.waitForKey()
        return
    
    def reboot(tpil):
        """Reboot the system"""
        terminal = tpil.gui.screenConsole()
        terminal.addText("Rebooting the system...")
        getoutput("reboot")
        return
   