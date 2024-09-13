import os
import json

data_folder = "data"
output_file = "wystawcy_all.txt"


issuers = set()

for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            data = json.loads(line)
            issuers.add(data["issuer"])
            
        
num_records = 0
with open(output_file, "w", encoding="utf-8") as file:
    for issuer in issuers:
        if issuer is not None:  
            file.write(issuer + "\n")
            num_records += 1
            
            
print("Liczba rekordow:", num_records)     
