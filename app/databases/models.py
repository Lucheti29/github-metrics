from sqlalchemy import Column, Integer, String, Date, DateTime

from utils.sql import Base

class Contributor(Base):
    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date)

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    #squad
    #skill
    startdate = Column(Date, nullable=False)
    enddate = Column(Date, nullable=False)
    hours = Column(Integer, nullable=False)
    #contributor

class Squad(Base):
    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    #category

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_name = Column(String, nullable=False)
    pull_request_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    github_user = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    closed_at = Column(DateTime)
    reviews_count = Column(Integer, nullable=False)
    status = Column(String, nullable=False)