#!/usr/bin/python3

# New design
#	Put all vocabulary in a single intermediate file with additional columns:
#	- duplicate(bool)
#	- book(text)
#	- 

import csv
import os
from source.models import Word

def resolveDuplicates(word):
	dupeList = []
	i = 0
	for item in word.getPotentialDuplicates():
		print(str(i + 1) + "\t" + item.kana + "|" + item.kanji + "|" + item.definition + "|" + item.book)
		i += 1
		dupeList.append(item)
	print("Item:\t" + word.kana + "|" + word.kanji + "|" + word.definition + "|" + word.book)
	print('Select item this is a duplicate of (d) or an owner of (o), or continue (c)')
	print('Examples: d15, o3, c')
	while(True):
		command = input('>')
		command = command.strip()
		if command[0] == 'd':
			word.owner = dupeList[int(command[1:]) - 1]
			break
		elif command[0] == 'o':
			dupeList[int(command[1:]) - 1].owner = word
			dupeList[int(command[1:]) - 1].save()
			break
		elif command[0] == 'c':
			word.owner_id = 0
			break
	word.save()
	
def parse(filepath, folder):
	data = []
	with open(filepath, newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			w = Word(kana = row[0], kanji = row[1], definition = row[2], book = folder)
			if w.alreadyExists():
				continue
			elif w.isDupe():
				resolveDuplicates(w)
			else:
				w.save()

for (path, dirs, files) in os.walk('./vocab'):
	book = path.split('./vocab')[1][1:]
	for filename in files:
		filepath = os.path.join(path, filename)
		filedata = parse(filepath, book)
