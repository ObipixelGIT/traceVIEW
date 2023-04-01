# -*- coding: utf-8 -*-
# Author : Dimitrios Zacharopoulos
# All copyrights to Obipixel Ltd
# 01 April 2023

#!/usr/bin/env python3

import re
import subprocess
import requests
import simplekml


# Print ASCII art
print("""
░▀█▀▒█▀▄▒▄▀▄░▄▀▀▒██▀░█▒█░█▒██▀░█░░▒█
░▒█▒░█▀▄░█▀█░▀▄▄░█▄▄░▀▄▀░█░█▄▄░▀▄▀▄▀
""")

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
