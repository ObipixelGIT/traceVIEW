# traceVIEW
traceVIEW performs a traceroute on a domain, extracts the IP Addresses from the path and generates a Google Earth KML file to view and analyse for OSINT research.

## How does the script work?

traceVIEW performs a traceroute to a given domain, extracts the IP addresses returned by the traceroute, and uses the IP-API service to query the location of each IP address. It then generates a KML file that displays the location of each IP address as a point on a map, and connects the points with a line to show the path taken by the traceroute.

### Code breakdown

- The re, subprocess, requests, and simplekml modules are imported.
- An ASCII art text is printed to the console for visual effect.
- The user is prompted to enter a domain name.
- The tcptraceroute command is run with the domain name provided by the user as the argument, and the output is saved to a file named traceVIEW-[domain]-log.txt.
- The IP addresses returned by the traceroute are extracted from the traceVIEW-[domain]-log.txt file using a regular expression, and stored in a list named ip_addresses.
- The IP-API service is queried for the location of each IP address in the ip_addresses list, and the latitude and longitude of each IP address are added to a KML file using the simplekml module.
- A line string is added between each pair of points in the KML file to show the path taken by the traceroute.
- A report is printed to the console showing the domain name being traced.
- The KML file is saved as traceVIEW-[domain]-map.kml.
- A message is printed to the console indicating that the traceroute results and KML file have been generated and saved to disk.
- *** a sample KML has been attached from a domain trace of: bbc.com (traceVIEW-bbc.com-map.kml)

## Preparation

The following Python modules must be installed:
```bash
pip3 install re, subprocess, requests, simplekml
```

The tcptraceroute command-line tool must be installed on the system. This tool is used to perform the traceroute over TCP. This can be done as follows:
- Windows: https://elifulkerson.com/projects/tcproute.php
- Linux: https://linuxcommandlibrary.com/man/tcptraceroute
- Mac OS: ```brew install tcptraceroute```

- The system running this script must have internet connectivity to query the IP-API service(http://ip-api.com) to obtain the location information for each IP address.

## Permissions

Ensure you give the script permissions to execute. Do the following from the terminal:
```bash
sudo chmod +x traceVIEW.py
```

## Usage
```bash
sudo python3 traceVIEW.py
```

## Sample script
```python
import re
import subprocess
import requests
import simplekml

# Prompt user for domain name
domain = input("Enter domain: ")

print()
print('\033[1;41m TRACEROUTE TO: '+domain+' \033[m')
print()

# Run tcptraceroute command and save output to file
trace = subprocess.Popen(["tcptraceroute", domain], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
with open('traceVIEW-'+domain+'-log.txt', 'w') as f:
    for line in iter(trace.stdout.readline, b''):
        f.write(line.decode('utf-8'))
        print(line.decode('utf-8').strip())

# Read the file and extract IP addresses
ip_addresses = []
with open('traceVIEW-'+domain+'-log.txt', 'r') as f:
    for line in f:
        match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        if match:
            ip_addresses.append(match.group())

# Query IP-API service for location of each IP address and add to KML file
kml = simplekml.Kml()
points = []
for ip in ip_addresses:
    response = requests.get(f"http://ip-api.com/json/{ip}")
    if response.status_code == 200:
        data = response.json()
        if 'lat' in data:
            lat = data['lat']
            lon = data['lon']
            kml.newpoint(name=ip, coords=[(lon, lat)])
            # Add the latitude and longitude of the IP address to the points list
            points.append((lat, lon))
        else:
            print(f"No location data for {ip}")
    else:
        print(f"Failed to retrieve location for {ip}")

# Add a line string between each pair of points
for i in range(len(points)-1):
    p1 = points[i]
    p2 = points[i+1]
    line = kml.newlinestring(name=f"{ip_addresses[i]} - {ip_addresses[i+1]}", coords=[(p1[1], p1[0]), (p2[1], p2[0])])
    line.style.linestyle.color = 'ff0000ff'  # Set line color to blue
    line.style.linestyle.width = 3  # Set line width to 3 pixels


print()
print('\033[1;41m TRACEROUTE REPORTING FOR: '+domain+' \033[m')
print()

# Write KML file
kml.save('traceVIEW-'+domain+'-map.kml')

print("Traceroute results written to traceVIEW-"+domain+"-log.txt file.")
print("KML file generated and written to traceVIEW-"+domain+"-map.kml file.")
```

## Sample output
```
sudo python3 traceVIEW.py
Password:

░▀█▀▒█▀▄▒▄▀▄░▄▀▀▒██▀░█▒█░█▒██▀░█░░▒█
░▒█▒░█▀▄░█▀█░▀▄▄░█▄▄░▀▄▀░█░█▄▄░▀▄▀▄▀

Enter domain: bbc.com

 TRACEROUTE TO: bbc.com

Selected device en0, address 192.168.1.173, port 64578 for outgoing packets
Tracing the path to bbc.com (151.101.0.81) on TCP port 80 (http), 30 hops max
1  192.168.1.254  2.235 ms  1.860 ms  1.937 ms
2  * * *
3  * * 31.55.186.177 11.557 ms
4  31.55.186.176  19.182 ms  9.753 ms  10.123 ms
5  213.121.192.144  11.347 ms  10.574 ms  10.546 ms
6  peer2-et0-1-6.slough.ukcore.bt.net (62.6.201.25)  10.697 ms  10.880 ms  12.807 ms
7  * * *
8  151.101.0.81 [open]  15.410 ms  10.674 ms *
No location data for 192.168.1.173
No location data for 192.168.1.254

 TRACEROUTE REPORTING FOR: bbc.com

Traceroute results written to traceVIEW-bbc.com-log.txt file.
KML file generated and written to traceVIEW-bbc.com-map.kml file.
```

## Disclaimer
"The scripts in this repository are intended for authorized security testing and/or educational purposes only. Unauthorized access to computer systems or networks is illegal. These scripts are provided "AS IS," without warranty of any kind. The authors of these scripts shall not be held liable for any damages arising from the use of this code. Use of these scripts for any malicious or illegal activities is strictly prohibited. The authors of these scripts assume no liability for any misuse of these scripts by third parties. By using these scripts, you agree to these terms and conditions."

## License Information

This library is released under the [Creative Commons ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/). You are welcome to use this library for commercial purposes. For attribution, we ask that when you begin to use our code, you email us with a link to the product being created and/or sold. We want bragging rights that we helped (in a very small part) to create your 9th world wonder. We would like the opportunity to feature your work on our homepage.
