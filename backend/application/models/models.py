from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
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
    password = Column(LargeBinary, nullable=False)
    created_at = Column(String, nullable=False)
    
    # groups = relationship('Group', secondary=User_Group, backref='members', lazy=True)
    words = relationship('UserWord', backref='user', lazy=True)
    stats = relationship('UserStat', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, email: str, password: bytes) -> None:
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
    password = Column(LargeBinary, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    def __init__(self, first_name: str, last_name: str, email: str, password: bytes, token: str = ""):
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
    definition = Column(String(length=300), nullable=False)
    created_at = Column(String, nullable=False)
    
    def __init__(self, word: str, word_type: str, definition: str) -> None: 
        self.word = word
        self.word_type = word_type 
        self.definition = definition 
        self.created_at = datetime.utcnow() 

class UserWord(Base):
    __tablename__ = 'user_word'
    word_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    word = Column(String, nullable=False)
    word_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    definition = Column(String(length=300), nullable=False)
    translated_language = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    correct = Column(Integer, nullable=False)
    incorrect = Column(Integer, nullable=False)

    def __init__(self, user_id: int, word: str, word_type: str, category: str, definition: str, translated_language: str, translation: str) -> None:
        self.user_id = user_id 
        self.word = word
        self.word_type = word_type 
        self.category = category
        self.definition = definition  
        self.translated_language = translated_language
        self.translation = translation
        self.created_at = datetime.utcnow()
        self.correct = 0 
        self.incorrect = 0 


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

class ResetPassword(Base): 
    __tablename__ = 'reset_password'

    reset_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    token = Column(LargeBinary, nullable=False)
    current_date = Column(String, nullable=False)

    def __init__(self, token: bytes, email: str):
        self.token = token 
        self.email = email 
        self.current_date = datetime.utcnow() 