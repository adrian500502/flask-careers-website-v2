from sqlalchemy import create_engine, text
import os

DATABASE_CONNECTION_STRING = os.environ.get('DATABASE_CONNECTION_STRING')

engine = create_engine(DATABASE_CONNECTION_STRING)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []

    for row in result.all():
      jobs.append(dict(row))
    
    return jobs