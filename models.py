from sqlalchemy import create_engine, ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import path, getcwd

engine = create_engine('sqlite:///' + path.join(getcwd(), 'data.db'))
Base = declarative_base()

class Resolution(Base):
    __tablename__ = 'resolutions'
    
    word1_id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    word2_id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    UniqueConstraint('word1_id', 'word2_id')
    
    def __init__(self, word1, word2):
        self.word1_id = word1.id
        self.word2_id = word2.id
        
    def save(self):
        session.add(self)
        session.commit()

    def alreadyExists(self):
        if self.id == None and session.query(Resolution).filter(Resolution.word1_id == self.word1.id, Resolution.word2_id == self.word2.id).union(
                               session.query(Resolution).filter(Resolution.word1_id == self.word2.id, Resolution.word2_id == self.word1.id)).count() > 0:
            return True
        else:
            return False
    
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

    def __init__(self, kana=None, definition=None, kanji=None, book=None, chapter=None, section=None):
        self.kana = kana
        self.kanji = kanji
        self.definition = definition
        self.book = book
        self.chapter = chapter
        self.section = section
    
    def __repr__(self):
        return "<Word(kana='%s', kanji='%s', definition='%s', book='%s', chapter='%s', section='%s')>" % (self.kana, self.kanji, self.definition, self.book, self.chapter, self.section)
    
    def save(self):
        if self.alreadyExists():
            return
        session.add(self)
        session.commit()

    def getAllChildren(self):
        wordlist = []
        q = session.query(Word).filter(Word.owner_id == self.id).all()
        for word in q:
            wordlist.append(word)
            wordlist.extend(word.getAllChildren())

        return wordlist

    def minId(self):
        minId = self.id
        for word in self.getAllChildren():
            if minId > word.id:
                minId = word.id

        return minId
    
    def ownerOf(self, other):
        other.owner_id = self.id
        other.save()
    
    def dupeOf(self, other):
        self.owner_id = other.id
        self.save()
        
    def resolve(self, other):
        r = Resolution(self, other)
        r.save()

    def isResolved(self, otherId):
        if self.id == otherId:
            return True
            
        q = session.query(Resolution).filter(Resolution.word1_id == self.id, Resolution.word2_id == otherId).union(
            session.query(Resolution).filter(Resolution.word1_id == otherId, Resolution.word2_id == self.id))
        
        if q.count() > 0:
            return True
        else:
            return False
    
    def isDupe(self):
        if self.owner_id == None:
            return False
        else:
            return True 
    
    def alreadyExists(self):
        if self.id == None and session.query(Word).filter(Word.kana == self.kana, Word.kanji == self.kanji, Word.definition == self.definition).count() > 0:
            return True
        else:
            return False
        
    def getPotentialDuplicates(self):
        dupes = session.query(Word).filter(Word.kana != None, Word.kana.contains(self.kana), Word.owner_id == None)

        if self.kanji != '':
            dupes = dupes.union(session.query(Word).filter(Word.kanji != None, Word.kanji.contains(self.kanji), Word.owner_id == None))

        dupes = dupes.all()
        
        trueDupes = []
        for dupe in dupes:
            if self.isResolved(dupe.id):
                continue
            else:
                trueDupes.append(dupe)
        
        return trueDupes
        
    def toArray(self):
        return [self.minId(), self.kana, self.kanji, self.definition]
        
    def getAll():
        return session.query(Word).all()
        
    def totalCount():
        return session.query(Word).count()
        
    def dupeCount():
        return session.query(Word).filter(Word.owner_id != None).count()
        
    def relationshipCount():
        return session.query(Resolution).count()
        
    def getById(wordId):
        return session.query(Word).filter(Word.id == wordId).one()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
