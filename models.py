from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum
from flask_login import UserMixin

db = SQLAlchemy()

class Job(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    location = Column(String(120), nullable=False)
    salary = Column(String(20), nullable=False)
    currency = Column(String(10), nullable=False)
    responsibilities = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'salary': self.salary,
            'currency': self.currency,
            'responsibilities': self.responsibilities,
            'requirements': self.requirements
        }
    
class User(db.Model, UserMixin):
  id = Column(Integer, primary_key=True)
  first_name = Column(String(150), nullable=False)
  last_name = Column(String(150), nullable=False)
  email = Column(String(150), unique=True, nullable=False)
  password = Column(String(150), nullable=False)
  is_admin = Column(Boolean, default=False)
  applications = db.relationship('Application', backref='user', lazy=True)

  def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'applications': [Application.to_dict() for app in self.applications]
        }

class Application(db.Model):
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), nullable=False)
    linkedin_url = Column(String(200), nullable=False)
    education = Column(Text, nullable=False)
    work_experience = Column(Text, nullable=False)
    resume_url = Column(String(200), nullable=False)
    status = Column(Enum('Pending', 'Accepted', 'Rejected', name='application_status'), default='Pending')
    job = db.relationship('Job', backref='applications')

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'linkedin_url': self.linkedin_url,
            'education': self.education,
            'work_experience': self.work_experience,
            'resume_url': self.resume_url,
            'status': self.status
        }
