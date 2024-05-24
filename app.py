from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

@app.route("/")
def enter_home():
  jobs = load_jobs_from_db()
  return render_template("home.html", jobs=jobs)

@app.route("/job/<id>")
def show_job(id):
  fetched_job = load_job_from_db(id)

  if not fetched_job:
    return "Not Found", 404
  return render_template("jobpage.html", job=fetched_job)

@app.route("/job/<id>/apply", methods=['POST'])
def apply_to_job(id):
  data = request.form
  fetched_job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template("application_submitted.html", application=data, job=fetched_job)

# JSON data /api/ endpoints
@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/api/job/<id>")
def list_job(id):
  fetched_job = load_job_from_db(id)

  if not fetched_job:
    return "Not Found", 404
  return jsonify(fetched_job)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8000)