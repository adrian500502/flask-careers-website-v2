from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
  {
    'id': 1,
    'title': "Data Analyst",
    'location': "Warsaw, Poland",
    'salary': 'PLN 10000'
  },
  {
    'id': 2,
    'title': "Data Scientist",
    'location': "Lodz, Poland",
    'salary': 'PLN 13450'
  },
  {
    'id': 3,
    'title': "Frontend engineer",
    'location': "San Francisco, USA",
    'salary': '$ 5250'
  },
]

@app.route("/")
def hello_world():
  return render_template("home.html", jobs=JOBS, company_name="Company")

@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8000)