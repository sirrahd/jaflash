#!/usr/bin/python3

import csv
import os
import sys
from models import Word

recordsCount = len(Word.getAll())
existsRecords = 0
newRecords = 0

def makeComboItem(word1, word2):
	global newRecords
	
	notDone = True
	while(notDone):
		print("Make an entry to combine the following words:")
		print(word1)
		print(word2)
		kana = input('kana>')
		kanji = input('kanji>')
		definition = input('definition>')
		
		word = Word(kana = kana, kanji = kanji, definition = definition)
		print(word)
		if 'y' == input("Is this correct? (y/n) "):
			notDone = False
			word.save()
			newRecords += 1
			word1.owner = word
			word1.save()
			word2.owner = word
			word2.save()

def resolveDuplicates(word):
	global recordsCount
	global existsRecords
	global newRecords
	
	print(str(recordsCount) + " starting records")
	print(str(existsRecords) + " already exist, " + str(newRecords) + " new records")
	
	dupeList = []
	i = 0
	for item in word.getPotentialDuplicates():
		print(str(i + 1) + "\t" + str(item))
		i += 1
		dupeList.append(item)
	print("Item:\t" + str(word))
	print('Select item this is (d)uplicate or (o)wner of, (m)ake a new item combining two, (c)ontinue, or (q)uit')
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
		elif command[0] == 'm':
			makeComboItem(word, dupeList[int(command[1:]) - 1])
			break
		elif command[0] == 'c':
			break
		elif command[0] == 'q':
			sys.exit()
	word.save()

def parse(filepath, folder, chapter, section):
	global recordsCount
	global existsRecords
	global newRecords
	
	data = []
	with open(filepath, newline='', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			w = Word(kana = row[0], kanji = row[1], definition = row[2], book = folder, chapter = chapter, section = section)
			if w.alreadyExists():
				existsRecords += 1
				continue
			elif w.isDupe():
				resolveDuplicates(w)
				newRecords += 1
			else:
				newRecords += 1
				w.save()

for (path, dirs, files) in os.walk('./vocab'):
	book = path.split('./vocab')[1][1:]
	for filename in files:
		filepath = os.path.join(path, filename)
		chapter = str(int(filename.split('.')[0]))
		section = filename.split('.')[1]
		filedata = parse(filepath, book, chapter, section)
	
print("All done building database. Results:")
print(str(recordsCount) + " starting records")
print(str(existsRecords) + " already exist, " + str(newRecords) + " new records")
