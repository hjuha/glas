from application import db
from application.models import Base

class Poll(Base):
	name = db.Column(db.String(100), nullable = False)
	description = db.Column(db.String(2000), nullable = False)
	first_question = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = True, index = True)
	questions = db.relationship("Question", backref = "poll", lazy = True, primaryjoin="Poll.id==Question.poll_id")

	def __init__(self, name, description, first_question):
		self.name = name
		self.description = description
		self.first_question = first_question

class Question(Base):
	text = db.Column(db.String(150), nullable = False)
	question_type = db.Column(db.String(12), nullable = False)
	poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"), nullable = False, index = True)
	successor = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = True, index = True)
	options = db.relationship("Option", backref = "question", lazy = True)
	sliders = db.relationship("Slider", backref = "question", lazy = True)

	def __init__(self, text, question_type, poll_id, successor):
		self.text = text
		self.question_type = question_type
		self.poll_id = poll_id
		self.successor = successor

class Slider(Base):
	left_text = db.Column(db.String(150), nullable = False)
	right_text = db.Column(db.String(150), nullable = False)
	question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = False, index = True)

	def __init__(self, left_text, right_text, question_id):
		self.left_text = left_text
		self.right_text = right_text
		self.question_id = question_id

class Option(Base):
	text = db.Column(db.String(250), nullable = False)
	question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = False, index = True)

	def __init__(self, text, question_id):
		self.text = text
		self.question_id = question_id