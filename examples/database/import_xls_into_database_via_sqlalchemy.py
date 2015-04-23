"""
imort_xls_into_database_via_sqlalchemy.py

:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This code snippet shows you how to import data from an excel
file into a database table via sqlalchemy

created along with pyexcel v0.1.5. 
"""
import os
import pyexcel
import pyexcel.ext.xls
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column , Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///birth.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# here is the destination table
class BirthRegister(Base):
    __tablename__='birth'
    id=Column(Integer, primary_key=True)
    name=Column(String)
    weight=Column(Float)
    birth=Column(Date)

Base.metadata.create_all(engine)

# create fixture
data = [
   ["name", "weight", "birth"],
   ["Adam", 3.4, datetime.date(2015, 2, 3)],
   ["Smith", 4.2, datetime.date(2014, 11, 12)]
]
pyexcel.save_as(array=data, dest_file_name="birth.xls")

# import the xls file
session = Session() # obtain a sql session
pyexcel.save_as(file_name="birth.xls",
                dest_session=session,
                dest_table=BirthRegister)

# verify results
sheet = pyexcel.get_sheet(session=session, table=BirthRegister)
print(sheet)

session.close()
os.unlink('birth.db')
os.unlink("birth.xls")