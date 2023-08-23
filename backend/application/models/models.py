from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association Tables 

# User_Group = Table('user_group', Base.metadata, 
#                    Column('user_id', Integer, ForeignKey('user.user_id')), 
#                    Column('group_id', Integer, ForeignKey('group.group_id'))
#                    )

# End of Association Tables 

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    
    # groups = relationship('Group', secondary=User_Group, backref='members', lazy=True)
    words = relationship('UserWord', backref='user', lazy=True)
    stats = relationship('UserStat', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, email: str, password: str) -> None:
        self.first_name = first_name 
        self.last_name = last_name 
        self.email = email 
        self.password = password 
        self.created_at = datetime.utcnow() 

class UnverifiedUser(Base):
    __tablename__ = 'unverified_user'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    def __init__(self, first_name: str, last_name: str, email: str, password: str, token: str = ""):
        self.email = email 
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.token = token
        self.created_at = datetime.utcnow()

class Word(Base): 
    __tablename__ = 'word'
    word_id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    word_type = Column(String, nullable=False)
    description = Column(String(length=50), nullable=False)
    definition = Column(String(length=300), nullable=False)
    created_at = Column(String, nullable=False)
    
    def __init__(self, word: str, word_type: str, description: str, definition: str) -> None: 
        self.word = word
        self.word_type = word_type 
        self.description = description 
        self.definition = definition 
        self.created_at = datetime.utcnow() 

class UserWord(Base):
    __tablename__ = 'user_word'
    word_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    word = Column(String, nullable=False)
    word_type = Column(String, nullable=False)
    description = Column(String(length=50), nullable=False)
    definition = Column(String(length=300), nullable=False)
    created_at = Column(String, nullable=False)
    correct = Column(String, nullable=False)
    incorrect = Column(String, nullable=False)

    def __init__(self, user_id: int, word: str, word_type: str, description: str, definition: str) -> None:
        self.user_id = user_id 
        self.word = word
        self.word_type = word_type 
        self.description = description 
        self.definition = definition  
        self.created_at = datetime.utcnow()
        self.correct = 0 
        self.incorrect = 0 

    def set_correct_incorrect(self, correct: int, incorrect: int) -> None: 
        self.correct = correct 
        self.incorrect = incorrect 

    def increment_correct(self) -> None:
        self.correct += 1 

    def increment_incorrect(self) -> None:
        self.incorrect += 1        

class UserStat(Base): 
    __tablename__ = 'user_stat'

    stat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    challenge_wins = Column(Integer, nullable=False)
    total_words_added = Column(Integer, nullable=False)
    total_words_practiced = Column(Integer, nullable=False)
    correct = Column(Integer, nullable=False)
    incorrect = Column(Integer, nullable=False)

    def __init__(self, user_id: int):
        self.user_id = user_id 
        self.challenge_wins = 0
        self.total_words_added = 0 
        self.total_words_practiced = 0 
        self.correct = 0 
        self.incorrect = 0 

# TODO: Create Group and Category tables 