# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    """
    description: Stores information about users who access the application.
    """
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

class Document(Base):
    """
    description: Stores metadata about uploaded scanned documents.
    """
    __tablename__ = 'document'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    uploaded_on = Column(DateTime, default=datetime.datetime.utcnow)

class Scan(Base):
    """
    description: Stores the scan images of documents.
    """
    __tablename__ = 'scan'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    image_path = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)

class EditableVersion(Base):
    """
    description: Stores editable text versions of the scanned documents.
    """
    __tablename__ = 'editable_version'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    content = Column(Text, nullable=False)
    version_number = Column(Integer, default=1)
    last_edited_on = Column(DateTime, default=datetime.datetime.utcnow)

class Annotation(Base):
    """
    description: Supports annotations made on document scans.
    """
    __tablename__ = 'annotation'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(Integer, ForeignKey('scan.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

class Comment(Base):
    """
    description: Stores comments made on editable versions of documents.
    """
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    editable_version_id = Column(Integer, ForeignKey('editable_version.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

class History(Base):
    """
    description: Tracks changes made to editable versions.
    """
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    editable_version_id = Column(Integer, ForeignKey('editable_version.id'), nullable=False)
    change_summary = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Tag(Base):
    """
    description: Stores tags for categorizing documents.
    """
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

class DocumentTag(Base):
    """
    description: Junction table for many-to-many relationship between documents and tags.
    """
    __tablename__ = 'document_tag'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

class Approval(Base):
    """
    description: Stores approval status for documents.
    """
    __tablename__ = 'approval'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('user.id'))
    status = Column(String, nullable=False, default='Pending')
    approved_on = Column(DateTime)

class AccessLog(Base):
    """
    description: Tracks user access of documents.
    """
    __tablename__ = 'access_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    accessed_on = Column(DateTime, default=datetime.datetime.utcnow)

class Role(Base):
    """
    description: Defines user roles within the application.
    """
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)

class UserRole(Base):
    """
    description: Junction table for many-to-many relationship between users and roles.
    """
    __tablename__ = 'user_role'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

# Database setup
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Creating a new session to insert sample data
Session = sessionmaker(bind=engine)
session = Session()

# Adding sample data
# Users
user1 = User(username="john_doe", email="john@example.com", password_hash="hashed_password_john")
user2 = User(username="jane_smith", email="jane@example.com", password_hash="hashed_password_jane")
session.add_all([user1, user2])

# Documents
document1 = Document(title="Document 1", description="First document description", created_by=1)
document2 = Document(title="Document 2", description="Second document description", created_by=2)
session.add_all([document1, document2])

# Scans
scan1 = Scan(document_id=1, image_path="/path/to/scan1.png", page_number=1)
scan2 = Scan(document_id=1, image_path="/path/to/scan2.png", page_number=2)
session.add_all([scan1, scan2])

# Editable Versions
editable_version1 = EditableVersion(document_id=1, content="Editable content for document 1", version_number=1)
editable_version2 = EditableVersion(document_id=2, content="Editable content for document 2", version_number=1)
session.add_all([editable_version1, editable_version2])

# Annotations
annotation1 = Annotation(scan_id=1, content="Annotation 1 for Scan 1", created_by=1)
annotation2 = Annotation(scan_id=2, content="Annotation 2 for Scan 1", created_by=2)
session.add_all([annotation1, annotation2])

# Comments
comment1 = Comment(editable_version_id=1, content="Comment 1 on Editable Version 1", created_by=1)
comment2 = Comment(editable_version_id=2, content="Comment 2 on Editable Version 2", created_by=2)
session.add_all([comment1, comment2])

# Histories
history1 = History(editable_version_id=1, change_summary="Initial creation")
history2 = History(editable_version_id=2, change_summary="Initial creation")
session.add_all([history1, history2])

# Tags
tag1 = Tag(name="Legal")
tag2 = Tag(name="Financial")
session.add_all([tag1, tag2])

# Document Tags
document_tag1 = DocumentTag(document_id=1, tag_id=1)
document_tag2 = DocumentTag(document_id=2, tag_id=2)
session.add_all([document_tag1, document_tag2])

# Approvals
approval1 = Approval(document_id=1, status="Approved", approved_by=2, approved_on=datetime.datetime.utcnow())
approval2 = Approval(document_id=2, status="Pending")
session.add_all([approval1, approval2])

# Access Logs
access_log1 = AccessLog(user_id=1, document_id=1)
access_log2 = AccessLog(user_id=2, document_id=2)
session.add_all([access_log1, access_log2])

# Roles
role1 = Role(name="Admin", description="Administrator with full access")
role2 = Role(name="Editor", description="Can edit documents")
session.add_all([role1, role2])

# User Roles
user_role1 = UserRole(user_id=1, role_id=1)
user_role2 = UserRole(user_id=2, role_id=2)
session.add_all([user_role1, user_role2])

# Commit changes
session.commit()
