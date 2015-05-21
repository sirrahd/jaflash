from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path, getcwd

engine = create_engine('sqlite:///' + path.join(getcwd(), 'data.db'))
Base = declarative_base()

class Word(Base):
	__tablename__ = 'words'
	
	id = Column(Integer, primary_key=True)
	kana = Column(String)
	kanji = Column(String)
	definition = Column(String)
	book = Column(String)
	chapter = Column(String)
	section = Column(String)
	owner_id = Column(Integer, ForeignKey('words.id'))
	owner = relationship('Word', backref='parent', remote_side='Word.id')
	
	def __init__(self, kana=None, kanji=None, definition=None, book=None, chapter=None, section=None):
		self.kana = kana
		self.kanji = kanji
		self.definition = definition
		self.book = book
		self.chapter = chapter
		self.section = section
	
	def __repr__(self):
		return "<Word(kana='%s', kanji='%s', definition='%s', book='%s', chapter='%s', section='%s')>" % (self.kana, self.kanji, self.definition, self.book, self.chapter, self.section)
	
	def save(self):
		session.add(self)
		session.commit()

	def isDupe(self):
		if self.owner:
			return True
		elif len(self.getPotentialDuplicates()):
			return True
		else:
			return False
			
	def getDupe(self):
		if self.owner_id:
			return getById(self.duplicate_id)
		else:
			return None
	
	def alreadyExists(self):
		if session.query(Word).filter(Word.kana == self.kana, Word.kanji == self.kanji, Word.definition == self.definition).count() > 0:
			return True
		else:
			return False
		
	def getPotentialDuplicates(self):
		dupes = session.query(Word).filter(Word.kana != None, Word.kana.contains(self.kana), Word.owner_id == None)
		if self.kanji != '':
			dupes.union(session.query(Word).filter(Word.kanji != None, Word.kanji.contains(self.kanji), Word.owner_id == None))
		if self.definition != '':
			dupes.union(session.query(Word).filter(Word.definition != None, Word.definition.contains(self.definition), Word.owner_id == None))
		
		return dupes.all()
		
	def getAll():
		return session.query(Word).all()
		
	def getById(wordId):
		return session.query(Word).filter(Word.id == wordId).one()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()