import os
from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_path = os.environ['DATABASE_URL']

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
  __tablename__ = 'Movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String)
  release_date = Column(db.Integer)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()    

class Actor(db.Model):
  __tablename__ = 'Actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  age = Column(db.Integer)
  gender = Column (db.String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()