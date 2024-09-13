import json
import certstream
import datetime
import sys
import time
import os


def write_to_file(records, file_path):
	folder_path = "data"
	os.makedirs(folder_path, exist_ok=True) 
	file_path = os.path.join(folder_path, file_path) 

	with open(file_path, "w") as file:
		for record in records:
		
			domain = record['data']['leaf_cert']['all_domains'][0]
			issuer = record['data']['leaf_cert']['issuer']['O']
			timestamp = record['data']['cert_index']

			domain_parts = domain.split('.')
			tld = domain_parts[-1]

			sld = domain_parts[-2]

			if sld in ["com", "gov", "edu", "org", "net", "mil"]:
				regdomain = domain_parts[-3] + '.' + sld + '.' + tld
			else:
				regdomain = sld + '.' + tld

			sld_tld = sld + '.' + tld

			json_data = {"timestamp": timestamp, "domain": domain, "regdomain": regdomain, "SLD_TLD": sld_tld, "SLD": sld, "TLD": tld, "issuer": issuer}
			file.write(json.dumps(json_data) + "\n")


def listen_for_certstream(num_files):
	count = 0
	records = []
	#url = "wss://certstream.calidog.io/"
	#url = "ws://192.168.51.63:4000/"
	def message_callback(message, context):
		nonlocal count
		if message['message_type'] == "certificate_update":
			records.append(message)
			if len(records) == 10000:
				now = datetime.datetime.now()
				timestamp_now = now.strftime('%Y-%m-%d_%H-%M-%S')
				file_path = f"certstream_{timestamp_now}.json"
				write_to_file(records, file_path)
				# time.sleep(10)
				count += 1
				print(count, ", ")
				records.clear()
				if count == num_files:
					sys.exit()


	#def on_open():
	    #print("Connection successfully established!")

	#def on_error(instance, exception):
	    #print("Exception in CertStreamClient! -> {}".format(exception))

	#certstream.listen_for_events(message_callback, on_open=on_open, on_error=on_error, url='wss://certstream.calidog.io/')
	certstream.listen_for_events(message_callback, url='wss://certstream.calidog.io/')



listen_for_certstream(2)

