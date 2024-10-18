# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 18, 2024 03:48:35
# Database: sqlite:////tmp/tmp.IjlimJ37fA/Test/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Role(SAFRSBaseX, Base):
    """
    description: Defines user roles within the application.
    """
    __tablename__ = 'role'
    _s_collection_name = 'Role'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    UserRoleList : Mapped[List["UserRole"]] = relationship(back_populates="role")



class Tag(SAFRSBaseX, Base):
    """
    description: Stores tags for categorizing documents.
    """
    __tablename__ = 'tag'
    _s_collection_name = 'Tag'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # parent relationships (access parent)

    # child relationships (access children)
    DocumentTagList : Mapped[List["DocumentTag"]] = relationship(back_populates="tag")



class User(SAFRSBaseX, Base):
    """
    description: Stores information about users who access the application.
    """
    __tablename__ = 'user'
    _s_collection_name = 'User'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_on = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    DocumentList : Mapped[List["Document"]] = relationship(back_populates="user")
    UserRoleList : Mapped[List["UserRole"]] = relationship(back_populates="user")
    AccessLogList : Mapped[List["AccessLog"]] = relationship(back_populates="user")
    ApprovalList : Mapped[List["Approval"]] = relationship(back_populates="user")
    AnnotationList : Mapped[List["Annotation"]] = relationship(back_populates="user")
    CommentList : Mapped[List["Comment"]] = relationship(back_populates="user")



class Document(SAFRSBaseX, Base):
    """
    description: Stores metadata about uploaded scanned documents.
    """
    __tablename__ = 'document'
    _s_collection_name = 'Document'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(ForeignKey('user.id'), nullable=False)
    uploaded_on = Column(DateTime)

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("DocumentList"))

    # child relationships (access children)
    AccessLogList : Mapped[List["AccessLog"]] = relationship(back_populates="document")
    ApprovalList : Mapped[List["Approval"]] = relationship(back_populates="document")
    DocumentTagList : Mapped[List["DocumentTag"]] = relationship(back_populates="document")
    EditableVersionList : Mapped[List["EditableVersion"]] = relationship(back_populates="document")
    ScanList : Mapped[List["Scan"]] = relationship(back_populates="document")



class UserRole(SAFRSBaseX, Base):
    """
    description: Junction table for many-to-many relationship between users and roles.
    """
    __tablename__ = 'user_role'
    _s_collection_name = 'UserRole'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    role_id = Column(ForeignKey('role.id'), nullable=False)

    # parent relationships (access parent)
    role : Mapped["Role"] = relationship(back_populates=("UserRoleList"))
    user : Mapped["User"] = relationship(back_populates=("UserRoleList"))

    # child relationships (access children)



class AccessLog(SAFRSBaseX, Base):
    """
    description: Tracks user access of documents.
    """
    __tablename__ = 'access_log'
    _s_collection_name = 'AccessLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    document_id = Column(ForeignKey('document.id'), nullable=False)
    accessed_on = Column(DateTime)

    # parent relationships (access parent)
    document : Mapped["Document"] = relationship(back_populates=("AccessLogList"))
    user : Mapped["User"] = relationship(back_populates=("AccessLogList"))

    # child relationships (access children)



class Approval(SAFRSBaseX, Base):
    """
    description: Stores approval status for documents.
    """
    __tablename__ = 'approval'
    _s_collection_name = 'Approval'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    document_id = Column(ForeignKey('document.id'), nullable=False)
    approved_by = Column(ForeignKey('user.id'))
    status = Column(String, nullable=False)
    approved_on = Column(DateTime)

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("ApprovalList"))
    document : Mapped["Document"] = relationship(back_populates=("ApprovalList"))

    # child relationships (access children)



class DocumentTag(SAFRSBaseX, Base):
    """
    description: Junction table for many-to-many relationship between documents and tags.
    """
    __tablename__ = 'document_tag'
    _s_collection_name = 'DocumentTag'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    document_id = Column(ForeignKey('document.id'), nullable=False)
    tag_id = Column(ForeignKey('tag.id'), nullable=False)

    # parent relationships (access parent)
    document : Mapped["Document"] = relationship(back_populates=("DocumentTagList"))
    tag : Mapped["Tag"] = relationship(back_populates=("DocumentTagList"))

    # child relationships (access children)



class EditableVersion(SAFRSBaseX, Base):
    """
    description: Stores editable text versions of the scanned documents.
    """
    __tablename__ = 'editable_version'
    _s_collection_name = 'EditableVersion'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    document_id = Column(ForeignKey('document.id'), nullable=False)
    content = Column(Text, nullable=False)
    version_number = Column(Integer)
    last_edited_on = Column(DateTime)

    # parent relationships (access parent)
    document : Mapped["Document"] = relationship(back_populates=("EditableVersionList"))

    # child relationships (access children)
    CommentList : Mapped[List["Comment"]] = relationship(back_populates="editable_version")
    HistoryList : Mapped[List["History"]] = relationship(back_populates="editable_version")



class Scan(SAFRSBaseX, Base):
    """
    description: Stores the scan images of documents.
    """
    __tablename__ = 'scan'
    _s_collection_name = 'Scan'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    document_id = Column(ForeignKey('document.id'), nullable=False)
    image_path = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)

    # parent relationships (access parent)
    document : Mapped["Document"] = relationship(back_populates=("ScanList"))

    # child relationships (access children)
    AnnotationList : Mapped[List["Annotation"]] = relationship(back_populates="scan")



class Annotation(SAFRSBaseX, Base):
    """
    description: Supports annotations made on document scans.
    """
    __tablename__ = 'annotation'
    _s_collection_name = 'Annotation'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scan.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime)

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("AnnotationList"))
    scan : Mapped["Scan"] = relationship(back_populates=("AnnotationList"))

    # child relationships (access children)



class Comment(SAFRSBaseX, Base):
    """
    description: Stores comments made on editable versions of documents.
    """
    __tablename__ = 'comment'
    _s_collection_name = 'Comment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    editable_version_id = Column(ForeignKey('editable_version.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(ForeignKey('user.id'), nullable=False)
    created_on = Column(DateTime)

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("CommentList"))
    editable_version : Mapped["EditableVersion"] = relationship(back_populates=("CommentList"))

    # child relationships (access children)



class History(SAFRSBaseX, Base):
    """
    description: Tracks changes made to editable versions.
    """
    __tablename__ = 'history'
    _s_collection_name = 'History'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    editable_version_id = Column(ForeignKey('editable_version.id'), nullable=False)
    change_summary = Column(Text)
    timestamp = Column(DateTime)

    # parent relationships (access parent)
    editable_version : Mapped["EditableVersion"] = relationship(back_populates=("HistoryList"))

    # child relationships (access children)
