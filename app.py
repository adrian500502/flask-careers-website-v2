from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from database import add_initial_data, load_jobs_from_db, load_job_from_db, add_application_to_db, load_applications_from_db, load_application_from_db, add_user_to_db
from models import db, Job, Application, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import case

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    add_initial_data()

@app.route("/")
def enter_home():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)

@app.route("/job/<int:id>")
def show_job(id):
    fetched_job = load_job_from_db(id)
    return render_template("jobpage.html", job=fetched_job) if fetched_job else "Not Found", 404

@app.route("/job/<int:id>/apply", methods=['POST'])
@login_required
def apply_to_job(id):
    data = request.form
    fetched_job = load_job_from_db(id)
    add_application_to_db(id, data, current_user.id)
    flash('Your application has been sent.', category='success')
    return render_template("application_submitted.html", application=data, job=fetched_job)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        add_user_to_db(user)
        login_user(user)
        flash('Account has been registered.', category='success')
        return redirect(url_for('enter_home'))
    
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in succesfully.', category='success')
            return redirect(url_for('enter_home'))
        else:
            flash('Incorrect credentials!', category='error')
        
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You\'ve been logged out.', category='info')
    return redirect(url_for('enter_home'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    if not current_user.is_admin:
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('enter_home'))

    if request.method == "POST":
        title = request.form.get('title')
        location = request.form.get('location')
        salary = request.form.get('salary')
        currency = request.form.get('currency')
        responsibilities = request.form.get('responsibilities')
        requirements = request.form.get('requirements')

        job = Job(
            title=title,
            location=location,
            salary=salary,
            currency=currency,
            responsibilities=responsibilities,
            requirements=requirements
        )
        db.session.add(job)
        db.session.commit()

        flash('Job offer added successfully.', 'success')
        return redirect(url_for('enter_home'))
    
    return render_template('add_job.html')

@app.route("/edit_job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    if not current_user.is_admin:
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('enter_home'))

    job = Job.query.get_or_404(job_id)

    if request.method == "POST":
        job.title = request.form.get('title')
        job.location = request.form.get('location')
        job.salary = request.form.get('salary')
        job.currency = request.form.get('currency')
        job.responsibilities = request.form.get('responsibilities')
        job.requirements = request.form.get('requirements')
        db.session.commit()
        
        flash('Job offer updated successfully.', 'success')
        return redirect(url_for('enter_home'))
    
    return render_template('edit_job.html', job=job)

@app.route("/delete_job/<int:job_id>", methods=["POST"])
@login_required
def delete_job(job_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('enter_home'))

    job = Job.query.get_or_404(job_id)
    applications = Application.query.filter_by(job_id=job.id).all()

    if applications:
        flash('Cannot delete job offer. There are applications associated with this job.', 'error')
        return redirect(url_for('enter_home'))

    db.session.delete(job)
    db.session.commit()
    
    flash('Job offer deleted successfully.', 'success')
    return redirect(url_for('enter_home'))



@app.route("/edit_application/<int:application_id>", methods=["POST"])
@login_required
def edit_application(application_id):
    data = request.form
    application = Application.query.filter_by(id=application_id, user_id=current_user.id).first()
    if application and application.status == 'Pending':
        application.full_name = data['full_name']
        application.email = data['email']
        application.linkedin_url = data['linkedin_url']
        application.education = data['education']
        application.work_experience = data['work_experience']
        application.resume_url = data['resume_url']
        db.session.commit()
        flash("Application has been updated.", category="success")
    else:
        flash("Application not found or you don't have permission to edit it.", "error")
    return redirect(url_for('profile'))

@app.route("/delete_application", methods=["POST"])
@login_required
def delete_application():
    application_id = request.form.get('application_id')
    application = Application.query.filter_by(id=application_id, user_id=current_user.id).first()
    if application and application.status == 'Pending':
        db.session.delete(application)
        db.session.commit()
    flash("Application deleted successfully.", "success")
    return redirect(url_for('profile'))

@app.route("/admin/applications")
@login_required
def admin_applications():
    if not current_user.is_admin:
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('enter_home'))

    status_order = case(
        (Application.status == 'Rejected', 1),
        (Application.status == 'Accepted', 2),
        (Application.status == 'Pending', 3),
    )

    applications = Application.query.order_by(
        status_order,
        Application.id.asc()
    ).all()
    return render_template("admin_applications.html", applications=applications)

@app.route("/accept_application", methods=["POST"])
@login_required
def accept_application():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('enter_home'))

    application_id = request.form.get('application_id')
    application = Application.query.filter_by(id=application_id).first()
    if application:
        application.status = 'Accepted'
        db.session.commit()
        flash('Application accepted.', 'success')
    else:
        flash('Application not found.', 'error')
    return redirect(url_for('admin_applications'))

@app.route("/reject_application", methods=["POST"])
@login_required
def reject_application():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'error')
        return redirect(url_for('enter_home'))

    application_id = request.form.get('application_id')
    application = Application.query.filter_by(id=application_id).first()
    if application:
        application.status = 'Rejected'
        db.session.commit()
        flash('Application rejected.', 'info')
    else:
        flash('Application not found.', 'error')
    return redirect(url_for('admin_applications'))


# JSON type data /api/ endpoints
@app.route("/api/jobs", methods=["GET", "POST"])
@login_required
def handle_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

@app.route("/api/jobs/<int:id>", methods=["GET"])
@login_required
def handle_job(id):
    fetched_job = load_job_from_db(id)
    return jsonify(fetched_job) if fetched_job else "Not Found", 404

# Applications
@app.route("/api/applications", methods=["GET"])
@login_required
def handle_applications():
    applications = load_applications_from_db()
    return jsonify(applications)

@app.route("/api/applications/<int:id>", methods=["GET"])
@login_required
def handle_application(id):
    fetched_application = load_application_from_db(id)
    return jsonify(fetched_application) if fetched_application else "Not Found", 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8111)
