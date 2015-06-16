#!/usr/bin/python3

import csv
import os
import sys
from models import Word

def makeComboItem(word1, word2):
    word = Word()
    while(word.id == None):
        print("Make an entry to combine the following words:")
        print(word1)
        print(word2)
        kana = input('kana>')
        kanji = input('kanji>')
        definition = input('definition>')
        
        word = Word(kana = kana, kanji = kanji, definition = definition)
        print(word)
        if 'y' == input("Is this correct? (y/n) "):
            word.save()
            word1.dupeOf(word)
            word2.dupeOf(word)
            
    return word

def resolveDuplicates(word, progressCount):
    global originalTotalCount
    global originalDupeCount
    global originalRelationshipCount
    
    if word.owner_id != None:
        return;
    
    dupes = word.getPotentialDuplicates()    
    while(len(dupes)):
        print(str(progressCount) + " of " + str(Word.totalCount()))
        print(str(Word.totalCount() - originalTotalCount) + " new words, " + str(Word.dupeCount() - originalDupeCount) + " new dupes, " + str(Word.relationshipCount() - originalRelationshipCount) + " new relationships")
        i = 1
        for item in dupes:
            print(str(i) + "\t" + str(item))
            i += 1
        print("Item:\t" + str(word))
        print('Select item this is (d)uplicate or (o)wner of, (m)ake a new item combining two, (c)ontinue, or (q)uit')
        command = input('>').strip()
        
        if command[0] == 'd':
            word.dupeOf(dupes[int(command[1:]) - 1])
            word = dupes[int(command[1:]) - 1]
        elif command[0] == 'o':
            word.ownerOf(dupes[int(command[1:]) - 1])
        elif command[0] == 'm':
            word = makeComboItem(word, dupes[int(command[1:]) - 1])
        elif command[0] == 'c':
            for dupe in dupes:
                word.resolve(dupe)
        elif command[0] == 'q':
            sys.exit()
        dupes = word.getPotentialDuplicates()

def populate(filepath, folder, chapter, section):
    data = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            Word(kana = row[0], kanji = row[1], definition = row[2], book = folder, chapter = chapter, section = section).save()

def writeToFile():
    with open('vocab.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for word in Word.getAll():
            if not word.isDupe():
                writer.writerow(word.toArray())
    csvfile.close()

originalTotalCount = Word.totalCount()
originalDupeCount = Word.dupeCount()
originalRelationshipCount = Word.relationshipCount()

for (path, dirs, files) in os.walk('./vocab'):
    book = path.split('./vocab')[1][1:]
    for filename in files:
        filepath = os.path.join(path, filename)
        chapter = str(int(filename.split('.')[0]))
        section = filename.split('.')[1]
        populate(filepath, book, chapter, section)
    
print("Database synced")
print(str(Word.totalCount() - originalTotalCount) + " new records, " + str(Word.totalCount()) + " total records")

i=1
for word in Word.getAll():
    resolveDuplicates(word, i)
    i += 1
    
print("Duplicates resolved")
print(str(Word.totalCount() - originalTotalCount) + " new words, " + str(Word.dupeCount() - originalDupeCount) + " new dupes, " + str(Word.relationshipCount() - originalRelationshipCount) + " new relationships")
print(str(Word.totalCount()) + " total words, " + str(Word.totalCount() - Word.dupeCount()) + " total originals, " + str(Word.dupeCount()) + " total dupes, " + str(Word.relationshipCount()) + " total relationships")

writeToFile();
print("vocab.csv created")