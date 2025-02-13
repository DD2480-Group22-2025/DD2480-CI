""" 
Small library for querying the build history database.
Uses SQLAlchemy ORM for database operations.
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///database/CI.db"
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

time_format = "%Y-%m-%d"

class BuildLog(Base):
    """SQLAlchemy model for build_log table"""
    __tablename__ = "build_log"
    
    id = Column(Integer, primary_key=True, index=True)
    commit_hash = Column(String, unique=True, nullable=False)
    branch = Column(String, nullable=False)
    build_date = Column(String, nullable=False)
    test_syntax_result = Column(String, nullable=False)
    test_notifier_result = Column(String, nullable=False)
    test_CI_result = Column(String, nullable=False)
    test_syntax_log = Column(String, nullable=False)
    test_notifier_log = Column(String, nullable=False)
    test_CI_log = Column(String, nullable=False)

def init_db():
    """Create database and tables if they don't exist"""
    os.makedirs("database", exist_ok=True)
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_entries():
    """Return a list of all existing build logs"""
    db = get_db()
    return [(entry.id, entry.commit_hash, entry.branch, entry.build_date, entry.test_syntax_result, entry.test_notifier_result, entry.test_CI_result, entry.test_syntax_log, entry.test_notifier_log, entry.test_CI_log) 
            for entry in db.query(BuildLog).all()]

def get_entry_by_commit(commit_hash: str):
    """Queries database for entry with specified hashsum"""
    db = get_db()
    entry = db.query(BuildLog).filter(BuildLog.commit_hash == commit_hash).first()
    return [(entry.id, entry.commit_hash, entry.branch, entry.build_date, entry.test_syntax_result, entry.test_notifier_result, entry.test_CI_result, entry.test_syntax_log, entry.test_notifier_log, entry.test_CI_log)] if entry else []

def get_entry_by_id(build_id: int):
    """Queries database for entry with specified id"""
    db = get_db()
    entry = db.query(BuildLog).filter(BuildLog.id == build_id).first()
    return [(entry.id, entry.commit_hash, entry.branch, entry.build_date, entry.test_syntax_result, entry.test_notifier_result, entry.test_CI_result, entry.test_syntax_log, entry.test_notifier_log, entry.test_CI_log)] if entry else []

def get_entries_by_date(build_date: str):
    """Queries database for all entries made on specified date"""
    db = get_db()
    entries = db.query(BuildLog).filter(BuildLog.build_date == build_date).all()
    return [(entry.id, entry.commit_hash, entry.branch, entry.build_date, entry.test_syntax_result, entry.test_notifier_result, entry.test_CI_result, entry.test_syntax_log, entry.test_notifier_log, entry.test_CI_log) for entry in entries]

def create_new_entry(commit_hash: str, branch: str, test_syntax_result: str, test_notifier_result: str, test_CI_result: str,
                    test_syntax_log: str, test_notifier_log: str, test_CI_log: str):
    """Create a new entry with a given commit hashsum and build logs"""
    db = get_db()
    build_date = datetime.today().strftime(time_format)
    
    # Check if entry already exists
    if db.query(BuildLog).filter(BuildLog.commit_hash == commit_hash).first():
        raise IntegrityError("Entry already exists", None, None)
    
    new_entry = BuildLog(
        commit_hash=commit_hash,
        branch=branch,
        build_date=build_date,
        test_syntax_result=test_syntax_result,
        test_notifier_result=test_notifier_result,
        test_CI_result=test_CI_result,
        test_syntax_log=test_syntax_log,
        test_notifier_log=test_notifier_log,
        test_CI_log=test_CI_log
    )
    db.add(new_entry)
    db.commit()
    return new_entry.id

# Initialize database on module import
init_db()
