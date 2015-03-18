#!/usr/bin/python3
import os
import csv

def formatLine(row, filetype):
	if filetype == 'kanji':
		row = [row['kanji'], " ".join([row['kana'], row['definition']])]
	elif filetype == 'vocab':
		if row['kanji'] != '':
			row = [row['kanji'], row['kana'], row['definition']]
		else:
			row = [row['kana'], '', row['definition']]
	return row

def make(outpath, filename, filetype, filedata):
	with open(os.path.join(outpath, filename), 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter='\t')
		for row in filedata:
			writer.writerow(formatLine(row, filetype))
	csvfile.close()


def parse(filepath):
	data = []
	with open(filepath, newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			dataline = { 'kana': row[0], 'kanji': row[1], 'definition': row[2] }
			if dataline not in data:
				data.append(dataline)
	csvfile.close()
	return data
			

for (path, dirs, files) in os.walk('./raw'):
	outpath = '.' + path.split('./raw')[1]
	if not os.path.exists(outpath):
		os.makedirs(outpath)
	for filename in files:
		filepath = os.path.join(path, filename)
		filetype = filename.split('.')[-2]
		print("Processing " + filepath)
		filedata = parse(filepath)
		make(outpath, filename, filetype, filedata)
