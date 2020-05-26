#Importing all the necessary modules
import re
import sys
import argparse


# Function to extract features from the raw log files
def extract_data(log_file):
	regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (.+) "(.*?)" "(.*?)"'
	data = {}
	#log file will be delivered from main.py
	for log_line in log_file:
		log_line=log_line.replace(',','_')
		log_line = re.match(regex,log_line).groups()
		size = str(log_line[4]).rstrip('\n')
		return_code = log_line[3]
		url = log_line[2]
		param_number = len(url.split('&'))
		url_length = len(url)
		if '-' in size:
			size = 0
		else:
			size = int(size)
		if (int(return_code) > 0):
			charcs = {}
			charcs['size'] = int(size)
			charcs['param_number'] = int(param_number)
			charcs['length'] = int(url_length)
			charcs['return_code'] = int(return_code)
			data[url] = charcs
	return data


# For more precise data, this module can be replaced and value can be added as 1 or 0 manually.
def label_data(data,labeled_data):
	for w in data:
		attack = '0'
		patterns = ['honeypot', '%3b', 'xss', 'sql', 'union', '%3c', '%3e', 'eval']
		if any(pattern in w.lower() for pattern in patterns):
			attack = '1'
		data_row = str(data[w]['length']) + ',' + str(data[w]['param_number']) + ',' + str(data[w]['return_code']) + ',' + attack + ',' + w + '\n'
		labeled_data.write(data_row)
	print (str(len(data)) + ' rows have successfully saved to ' + str(labeled_data.name))
	labeled_data.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--log_file', help = 'The raw http log file', required = True)
	parser.add_argument('-d', '--dest_file', help = 'Destination to store the resulting csv file', required = True)
	args = vars(parser.parse_args())

	log_file = args['log_file']
	dest_file = args['dest_file']

	label_data(extract_data(log_file),open(dest_file, 'w'))
