import csv
import subprocess

# Merge the Falcon CSV files using shell command
subprocess.run("cat falcon/*.csv > merged_falcon.csv", shell=True, check=True)

# Define the input and output file names
input_file = 'merged_falcon.csv'
output1_file = 'output1.csv'
output2_file = 'output2.csv'
final_output_file = 'falcon.csv'

# Define the columns to keep in each output file
columns_output1 = ['CVE ID', 'LocalIP', 'Remediation Details']
columns_output2 = ['CVE ID', 'Hostname', 'Remediation Details']

# Open the input CSV file and the two output CSV files
with open(input_file, 'r', newline='') as infile, \
     open(output1_file, 'w', newline='') as outfile1, \
     open(output2_file, 'w', newline='') as outfile2:

    # Create CSV reader and writer objects
    reader = csv.DictReader(infile)
    writer1 = csv.DictWriter(outfile1, fieldnames=columns_output1)
    writer2 = csv.DictWriter(outfile2, fieldnames=columns_output2)

    # Write headers to the output files
    writer1.writeheader()
    writer2.writeheader()

    # Iterate through each row in the input file
    for row in reader:
        # Create dictionaries with selected columns for each output file
        data1 = {col: row[col] for col in columns_output1}
        data2 = {col: row[col] for col in columns_output2}

        # Write the selected data to the output files
        writer1.writerow(data1)
        writer2.writerow(data2)

# Concatenate output1.csv and output2.csv into falcon.csv
subprocess.run(f"cat {output1_file} {output2_file} > {final_output_file}", shell=True, check=True)

# Clean up temporary files
subprocess.run(f"rm {output1_file} {output2_file} {input_file}", shell=True, check=True)

# Remove header lines from falcon.csv
subprocess.run("sed -i '/CVE ID,LocalIP,Remediation Details/d; /CVE ID,Hostname,Remediation Details/d' falcon.csv", shell=True, check=True)
subprocess.run("sed -i 's/.infra.paynet.my//g' falcon.csv", shell=True, check=True)
