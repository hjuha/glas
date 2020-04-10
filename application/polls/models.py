from application import db
from application.models import Base

class Poll(Base):
	name = db.Column(db.String(100), nullable = False)
	description = db.Column(db.String(2000), nullable = False)
	first_question = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = True, index = True)
	questions = db.relationship("Question", backref = "poll", lazy = True, primaryjoin="Poll.id==Question.poll_id")
	results = db.relationship("Result", backref = "poll", lazy = True)
	
	def __init__(self, name, description, first_question):
		self.name = name
		self.description = description
		self.first_question = first_question

class Question(Base):
	text = db.Column(db.String(400), nullable = False)
	question_type = db.Column(db.String(12), nullable = False)
	poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"), nullable = False, index = True)
	successor = db.Column(db.Integer, db.ForeignKey("question.id"), nullable = True, index = True)
	options = db.relationship("Option", backref = "question", lazy = True)
	sliders = db.relationship("Slider", backref = "question", lazy = True)
	maximum = db.Column(db.Integer)

	def __init__(self, text, question_type, poll_id, successor, maximum):
		self.text = text
		self.question_type = question_type
		self.poll_id = poll_id
		self.successor = successor
		self.maximum = maximum

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

class Result(Base):
	poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"), nullable = False, index = True)
	name = db.Column(db.String(150), nullable = False)
	description = db.Column(db.String(2000), nullable = False)
	image_path = db.Column(db.String(250), nullable = False)
	primary_color = db.Column(db.String(7), nullable = False)
	secondary_color = db.Column(db.String(7), nullable = False)
	option_results = db.relationship("OptionResult", backref = "Result", lazy = True)
	slider_results = db.relationship("SliderResult", backref = "Result", lazy = True)
	
	def __init__(self, poll_id, name, description, image_path, primary_color, secondary_color):
		self.poll_id = poll_id
		self.name = name
		self.description = description
		self.image_path = image_path
		self.primary_color = primary_color
		self.secondary_color = secondary_color

class OptionResult(Base):
	result_id = db.Column(db.Integer, db.ForeignKey("result.id"), nullable = False, index = True)
	option_id = db.Column(db.Integer, db.ForeignKey("option.id"), nullable = False, index = True)

	def __init__(self, result_id, option_id):
		self.result_id = result_id
		self.option_id = option_id

class SliderResult(Base):
	result_id = db.Column(db.Integer, db.ForeignKey("result.id"), nullable = False, index = True)
	slider_id = db.Column(db.Integer, db.ForeignKey("option.id"), nullable = False, index = True)
	value = db.Column(db.Integer)

	def __init__(self, result_id, slider_id, value):
		self.result_id = result_id
		self.slider_id = slider_id
		self.value = value
