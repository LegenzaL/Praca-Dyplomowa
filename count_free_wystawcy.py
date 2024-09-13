import os
import json

data_folder = "data"
dict_folder = os.path.join("slowniki", "wystawcy")
output_file = "results_wystawcy.json"

keywords = set()
for filename in os.listdir(dict_folder):
    with open(os.path.join(dict_folder, filename), "r") as f:
        for line in f:
            keywords.add(line.strip())

counts = {keyword: 0 for keyword in keywords}
total_records = 0
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            total_records += 1
            record = json.loads(line)
            for keyword in keywords:
                if record["issuer"] and keyword in record["issuer"]:
                    counts[keyword] += 1
                    
counts["TOTAL"] = total_records

# Output the results
with open(output_file, "w") as f:
    json.dump(counts, f)
