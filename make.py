import os

def kanji(fname, ipath, opath):
	print("Making kanji " + fname + " in " + opath);
	r = open(ipath + '/' + fname, encoding='utf-8')
	w = open(opath + '/' + fname, 'w', encoding='utf-8')

	lineCount = 0
	history = []
	for line in r:
		lineCount += 1
		line = line.strip()
		if line not in history:
			history.append(line)
			line = line.split('\t')
			try:
			    history.append(' '.join(line))
			    w.write(line[1] + '\t' + line[0] + ' ' + line[2] + '\n')
			except:
			    print('Error in line ' + str(lineCount) + '.\n')

	w.close()
	r.close()

def vocab(fname, ipath, opath):
	print("Making vocab " + fname + " in " + opath);
	r = open(ipath + '/' + fname, encoding='utf-8')
	w = open(opath + '/' + fname, 'w', encoding='utf-8')

	lineCount = 0
	for line in r:
		lineCount += 1
		output = ['','','']
		line = line.split('\t')
	    
		if line[1] != '':
			output[0] = line[1]
			output[1] = line[0]
		else:
			output[0] = line[0]
			output[1] = ''

		try:
			output[2] = line[2]
		except:
			print('Error in line ' + str(lineCount) + '.\n')

		w.write('\t'.join(output))

	w.close()
	r.close()

for (path, dirs, files) in os.walk('./raw'):
	fpath = '.' + path[5:]
	if not os.path.exists(fpath):
		os.makedirs(fpath)
	for fname in files:
		ftype = fname.split('.')[-2]
		if ftype == 'kanji':			
			kanji(fname, path, fpath)
		elif ftype == 'vocab':
			vocab(fname, path, fpath)
