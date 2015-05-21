from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path, getcwd

engine = create_engine('sqlite:///' + path.join(getcwd(), 'data.db'))
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Word(Base):
	__tablename__ = 'words'
	
	id = Column(Integer, primary_key=True)
	kana = Column(String)
	kanji = Column(String)
	definition = Column(String)
	duplicate_id = Column(Integer, ForeignKey('words.id'))
	duplicate = relationship('Word', backref='parent', remote_side='Word.id')
	
	def __repr__(self):
		return "<Word(kana='%s', kanji='%s', definition='%s')>" % (self.kana, self.kanji, self.definition)
	
	def save(self):
		session.add(self)
		session.commit()

	def isDupe(self):
		if self.duplicate_id:
			return True;
		else:
			return False;
			
	def getDupe(self):
		if self.duplicate_id:
			return getById(self.duplicate_id)
		else:
			return None
		
	def getPotentialDuplicates(self):
		dupes = []
		if self.kanji != '':
			dupes.append(session.query(Word).filter(Word.kanji == self.kanji).all())
		if self.kana != '':
			dupes.append(session.query(Word).filter(Word.kana == self.kana).all())
		if self.definition != '':
			dupes.append(session.query(Word).filter(Word.kana == self.kana).all())
		
		return dupes
		
	def getAll():
		return session.query(Word).all()
		
	def getById(wordId):
		return session.query(Word).filter(Word.id == wordId).one()
