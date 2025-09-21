🔐 maters Plugin Suite
A modular plugin set for PwnHyve designed to assist with wireless handshake capture, device discovery, and network casting. This suite offers a mix of offensive and utility tools for wireless auditing and local network interaction.
📦 Features
• 	Capture WPA handshakes using 
• 	Convert  files to Hashcat-compatible format
• 	Discover devices on the local network via ARP
• 	Share captured handshakes via HTTP
• 	Cast YouTube videos to all TVs on your network
• 	Test plugin functionality with a simple console message

🧩 Plugin Functions

A simple test to verify plugin integration with PwnHyve.
• 	✅ Displays a confirmation message in the terminal
• 	🛠️ Useful for debugging plugin loading


Captures WPA handshakes using .
• 	📡 Uses wlan1 interface (hardcoded) (requires an external adapter)
• 	🧪 Starts monitor mode via 
• 	📝 Saves output to 
• 	🛑 Stops capture on keypress



Converts all  files in the handshake folder to Hashcat format.
• 	🔄 Uses 
• 	📁 Input: 
• 	📤 Output:  file



Discovers devices on the local network using ARP packets.
• 	🌐 Uses  to determine base IP
• 	📡 Sends broadcast ARP requests to 
• 	📋 Displays IP and MAC of discovered devices



Shares handshake files via a simple HTTP server.
• 	🌍 Starts a Python HTTP server on port 
• 	📁 Serves 
• 	🛑 Attempts to kill server with 



Casts a YouTube video to all TVs on the network.
• 	📺 Uses  protocol and 
• 	🔍 Discovers devices via Zeroconf
• 	🎬 Launches YouTube with video ID 


🛠️ Requirements
• 	Python 3.11+
• 	pychromecast
• 	pylaunch
• 	netifaces
• 	scapy

🚧 TODOs
• 	Add dynamic interface selection
• 	Improve server shutdown logic
• 	Expand device discovery with port/service enumeration
• 	Add error handling and logging

🧠 Author
Created by Mater
Feel free to open issues or contribute improvements!

Let me know if you'd like this formatted as a Markdown file or want badges, install instructions, or screenshots added!
