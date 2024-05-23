from flask import Flask, render_template, jsonify
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__)

@app.route("/")
def enter_home():
  jobs = load_jobs_from_db()
  return render_template("home.html", jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  fetched_job = load_job_from_db(id)

  if not fetched_job:
    return "Not Found", 404
  
  return render_template("jobpage.html", job=fetched_job)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8000)