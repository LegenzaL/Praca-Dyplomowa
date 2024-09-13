import os
import json

data_folder = "data"
dict_folder1 = os.path.join("slowniki", "tld")
dict_folder2 = os.path.join("slowniki", "sld_tld")
output_file = "results_free_tld.json"

keywords1 = set()
for filename in os.listdir(dict_folder1):
    with open(os.path.join(dict_folder1, filename), "r") as f:
        for line in f:
            keywords1.add(line.strip())

keywords2 = set()
for filename in os.listdir(dict_folder2):
    with open(os.path.join(dict_folder2, filename), "r") as f:
        for line in f:
            keywords2.add(line.strip())


results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            if any(keyword == record["TLD"] for keyword in keywords1) or any(keyword == record["SLD_TLD"] for keyword in keywords2):
                results.append(record)
                
                
num_records = 0
with open(output_file, "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
        num_records += 1

print("Liczba rekordow:", num_records)        
