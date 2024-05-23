from sqlalchemy import create_engine, text
import os, sys

DATABASE_CONNECTION_STRING = os.environ.get('DATABASE_CONNECTION_STRING')

engine = create_engine(DATABASE_CONNECTION_STRING)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []

    for row in result.all():
      jobs.append(dict(row))
    
    return jobs
  
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from jobs where id={id}"))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])