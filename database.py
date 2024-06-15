from models import db, Job, User, Application

def add_initial_data():
    if Job.query.count() == 0:
        jobs = [
            Job(title="Software Engineer", location="Remote", salary="7000", currency="$", responsibilities="Develop software\nWrite tests", requirements="3 years experience\nPython knowledge"),
            Job(title="Data Scientist", location="New York", salary="9000", currency="PLN", responsibilities="Analyze data\nCreate models", requirements="2 years experience\nPython knowledge"),
            Job(title="Fullstack Developer", location="Warsaw", salary="12000", currency="PLN", responsibilities="Analyze data\nCreate models", requirements="5 years experience\nPython knowledge"),
            Job(title="Product Manager", location="San Francisco", salary="7500", currency="GBP", responsibilities="Manage product\nCommunicate with stakeholders", requirements="5 years experience\nProduct management experience"),
            Job(title="Frontend Developer", location="San Francisco", salary="6300", currency="GBP", responsibilities="Manage product\nCommunicate with stakeholders", requirements="5 years experience\nProduct management experience"),
            Job(title="Backend Developer", location="San Francisco", salary="6500", currency="GBP", responsibilities="Manage product\nCommunicate with stakeholders", requirements="5 years experience\nProduct management experience")
        ]
        db.session.add_all(jobs)
        db.session.commit()

    if User.query.count() == 0:
        user = User(first_name="Adam", last_name="Kowalski", email="admin@example.com", password="Admin123!", is_admin=True)
        db.session.add(user)
        db.session.commit()

# Jobs
def load_jobs_from_db():
    jobs = Job.query.all()
    return [job.to_dict() for job in jobs]

def load_job_from_db(id):
    job = Job.query.filter_by(id=id).first()
    return job.to_dict() if job else None

def post_job_to_db(data):
    job = Job(
        title=data['title'],
        location=data['location'],
        salary=data['salary'],
        currency=data['currency'],
        responsibilities=data['responsibilities'],
        requirements=data['requirements']
    )
    db.session.add(job)
    db.session.commit()

def put_job_in_db(id):
    pass
def patch_job_in_db(id):
    pass
def delete_job_from_db(id):
    pass

#Users
def add_user_to_db(user: User):
    db.session.add(user)
    db.session.commit()
    
#Applications
def add_application_to_db(job_id, data, user_id):
    application = Application(
        job_id=job_id,
        user_id=user_id,
        full_name=data['full_name'],
        email=data['email'],
        linkedin_url=data['linkedin_url'],
        education=data['education'],
        work_experience=data['work_experience'],
        resume_url=data['resume_url'],
        status='Pending'
    )
    db.session.add(application)
    db.session.commit()

def load_applications_from_db():
    applications = Application.query.all()
    return [application.to_dict() for application in applications]

def load_application_from_db(id):
    application = Application.query.filter_by(id=id).first()
    return application.to_dict() if application else None
    