# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData
import dotenv

values=dict(dotenv.dotenv_values('.env'))

user=values['USER']
passwd=values['PASSWD']
db=values['DB']
port=values['PORT']
host=values['HOST']

engine=create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}")
meta=MetaData()
conn=engine.connect()


