from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from banc import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20))
    fullname = db.Column(db.String())
    profession = db.Column(db.String(20))
    description = db.Column(db.String())
    languages = db.Column(db.String())
    home_address = db.Column(db.String())
    rate = db.Column(db.String())
    date_joined= db.Column(db.DateTime())
    skills = db.relationship('Skills',backref='skill',lazy=True)
    projects = db.relationship('Project',backref='project',lazy=True)
    ratings = db.relationship('Ratings',backref='ratin',lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None    
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}','{self.image_file}')"



#skills database class
class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Skill name('{self.skill_name}')"
    
#project details
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted= db.Column(db.DateTime())
    project_name = db.Column(db.String())
    project_description = db.Column(db.String())
    required_skills = db.Column(db.String())
    payment_type = db.Column(db.String())
    currencyy = db.Column(db.String())
    budget = db.Column(db.String())
    deadline = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bids = db.relationship('Bids',backref='bid',lazy=True)

    def __repr__(self):
        return f"Skill name('{self.project_name}')"
    

#bid details
class Bids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted= db.Column(db.DateTime())
    currencyy = db.Column(db.String())
    bidd = db.Column(db.String())
    duration = db.Column(db.String())
    payment_type = db.Column(db.String())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bid('{self.id}')"


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String())
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Rating('{self.id}')"


    