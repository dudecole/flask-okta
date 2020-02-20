from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __init__ import app
from flask_migrate import Migrate

# app.config.from_object(BaseConfig[''])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class RecentTasks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50), nullable=False)
    task_details = db.Column(db.String(500), nullable=True)
    task_stage = db.Column(db.String(50), nullable=True)
    task_requester = db.Column(db.String(50), nullable=True)
    task_approver = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #
    # def __init__(self, text):
    #     self.text = text
    #     self.date_posted = datetime.datetime.now()

    def __repr__(self):
        return '<Task %r>' % self.id

# class Post(db.Model):
#
#
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False)
#
#     def __init__(self, text):
#         self.text = text
#         self.date_posted = datetime.datetime.now()


