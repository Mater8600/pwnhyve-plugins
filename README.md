# 🔐 Mater's Plugin Suite

A modular plugin set for **PwnHyve** (https://github.com/whatotter/pwnhyve) designed to assist with wireless handshake capture, device discovery, and network casting.  
This suite offers a mix of offensive and utility tools for wireless auditing and local network interaction.

---

## 📦 Features

- Capture WPA handshakes using `hcxdumptool`
- Convert handshake files to Hashcat-compatible format
- Discover devices on the local network via ARP
- Share captured handshakes via HTTP
- Cast YouTube videos to all TVs on your network
- Test plugin functionality with a simple console message

---

## 🧩 Plugin Functions

### Test Plugin
A simple test to verify plugin integration with PwnHyve.

- ✅ Displays a confirmation message in the terminal  
- 🛠️ Useful for debugging plugin loading

---

### Capture WPA Handshakes
Captures WPA handshakes using `hcxdumptool`.

- 📡 Uses `wlan1` interface (hardcoded) — requires an external adapter  
- 🧪 Starts monitor mode via `airmon-ng`  
- 📝 Saves output to `/root/pwnhyve/handshakes/output.pcapng`  
- 🛑 Stops capture on keypress

---

### Convert Handshakes
Converts all handshake files in the handshake folder to Hashcat format.

- 🔄 Uses `hcxpcapngtool`  
- 📁 Input: `/root/pwnhyve/handshakes/*`  
- 📤 Output: `handshakes` file

---

### Discover Devices
Discovers devices on the local network using ARP packets.

- 🌐 Uses `netifaces` to determine base IP  
- 📡 Sends broadcast ARP requests to `<base_ip>.0/24`  
- 📋 Displays IP and MAC of discovered devices

---

### Share Handshakes
Shares handshake files via a simple HTTP server.

- 🌍 Starts a Python HTTP server on port `12969`  
- 📁 Serves `/root/pwnhyve/handshakes/`  
- 🛑 Attempts to kill server with `pkill http.server`

---

### Cast to TVs
Casts a YouTube video to all TVs on the network.

- 📺 Uses `Dial` protocol and `pychromecast`  
- 🔍 Discovers devices via Zeroconf  
- 🎬 Launches YouTube with video ID `dQw4w9WgXcQ`

---

## 🛠️ Requirements

- Python 3.11+
- [`pychromecast`](https://pypi.org/project/PyChromecast/)
- [`pylaunch`](https://pypi.org/project/pylaunch/)
- [`netifaces`](https://pypi.org/project/netifaces/)
- [`scapy`](https://pypi.org/project/scapy/)

---

## 🚧 TODOs

- Add dynamic interface selection  
- Improve server shutdown logic  
- Expand device discovery with port/service enumeration  
- Add error handling and logging

---

## 🧠 Author

Created by **Mater**  
Feel free to open issues or contribute improvements!
