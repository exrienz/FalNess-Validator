import csv
import subprocess
import os
import shutil

# Instructions
message = """
:::: Falcon & Nessus Finding Validator by Muzaffar Mohamed for Paynet ::::

How to use?
1. Retrieve the Nessus report, ensuring it contains only the CVE and Host columns, and store the files in the "nessus" directory.
2. Acquire the Falcon report and place it in the "falcon" folder.
3. Execute 'python3 validate.py', generating 'Validated.csv' with shared host and CVE entries from both the Falcon and Nessus reports.
"""

print(message)

# Directory names
directories = ["nessus", "falcon"]

# Create directories if they don't exist
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Check if each directory is empty
for directory in directories:
    if not os.listdir(directory):
        print(f"Status: The '{directory}' folder is empty. You need a report to proceed. Exiting the application.")
        exit(1)

# Concatenate nessus/*.csv files into nessus.csv
subprocess.run("cat nessus/*.csv > nessus.csv", shell=True, check=True)

# Remove unwanted lines and characters from nessus.csv
subprocess.run("sed -i -e '/CVE,Host/d; /\"\",\"/d' -e 's/\"//g' -e 's/.infra.paynet.my//g' nessus.csv", shell=True, check=True)

# Run falcon.py using Python3
subprocess.run("python3 falcon.py", shell=True, check=True)

# Read data from falcon.csv and create a dictionary with CVE as keys
falcon_data = {}
with open('falcon.csv', mode='r') as falcon_file:
    falcon_reader = csv.reader(falcon_file)
    next(falcon_reader)  # Skip the header row
    for row in falcon_reader:
        cve, ip, description = row
        falcon_data[cve] = {'ip': ip, 'description': description}
print("Status: Analyzing & Converting Report")

# Read data from nessus.csv and create a list of IPs for each CVE
nessus_data = {}
with open('nessus.csv', mode='r') as nessus_file:
    nessus_reader = csv.reader(nessus_file)
    next(nessus_reader)  # Skip the header row
    for row in nessus_reader:
        cve, ip = row
        nessus_data.setdefault(cve, []).append(ip)

# Now you can combine the data from both CSV files
combined_data = []
for cve, ips in nessus_data.items():
    if cve in falcon_data:
        description = falcon_data[cve]['description']
        combined_data.extend([[cve, ip, description] for ip in ips])

# Write the combined data to a new CSV file
with open('Validated.csv', mode='w', newline='') as combined_file:
    combined_writer = csv.writer(combined_file)
    combined_writer.writerow(['CVE', 'Host', 'Description'])
    combined_writer.writerows(combined_data)

print()
print("Status: Cleaning-up Leftover & Completed!")

# Remove all contents from each directory
for directory in directories:
    if os.path.exists(directory):
        shutil.rmtree(directory)
