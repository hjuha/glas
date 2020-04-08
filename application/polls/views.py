from flask import render_template, request, redirect, url_for

from application import app, db
from application.polls.models import Poll, Question, Slider, Option, Result, OptionResult, SliderResult

@app.route("/new/", methods = ["GET", "POST"])
def new_poll():
	if request.method == "GET":
		return render_template("polls/new.html")

	questions = []
	sliders = []
	options = []
	for key in request.form:
		if key[:8] == "question":
			sliders.append([])
			options.append([])
			q_id = key[8:]
			question = request.form[key]
			questions.append(question)
			if "left" + q_id in request.form:
				slider_left = request.form["left" + q_id]
				slider_right = request.form["right" + q_id]
				sliders[-1] = (slider_left, slider_right)
			else:
				for key_ in request.form:
					if key_[:7+len(q_id)] == "option" + q_id + "_":
						options[-1].append(request.form[key_])

	poll = Poll(request.form["title"], request.form["desc"], None)
	db.session().add(poll)
	db.session().commit()

	poll_id = poll.id
	i = len(questions) - 1
	prev_id = None
	while i >= 0:
		question = Question(questions[i], "slider" if sliders[i] else "multichoice", poll_id, prev_id)
		db.session().add(question)
		db.session().commit()
		prev_id = question.id
		if sliders[i]:
			slider = Slider(sliders[i][0], sliders[i][1], prev_id)
			db.session().add(slider)
			db.session().commit()
		for option_text in options[i]:
			option = Option(option_text, prev_id)
			db.session().add(option)
			db.session().commit()
		i -= 1

	poll.first_question = prev_id
	db.session().commit()

	return redirect(url_for("index"))

@app.route("/<poll_id>/answer", methods = ["GET", "POST"])
def answer_poll(poll_id):
	poll = Poll.query.get(poll_id)
	questions = []
	question = poll.first_question
	while question:
		questions.append(Question.query.get(question))
		question = questions[-1].successor

	if request.method == "GET":
		return render_template("polls/poll.html", poll=poll, questions=questions, answer=True)
	
	print(request.form)
	def hsv2rgb(t):
		if len(t) < 4:
			return "#FFFFFF"
		t = t[4:-1].split(", ")
		r = int(t[0])
		g = int(t[1])
		b = int(t[2])
		return '#%02x%02x%02x' % (r, g, b)
	primary = hsv2rgb(request.form["primary"])
	secondary = hsv2rgb(request.form["secondary"])
	result = Result(poll_id, request.form["name"], request.form["desc"], request.form["image"], primary, secondary)
	db.session().add(result)
	db.session().commit()

	for question in questions:
		if question.question_type == "slider":
			for slider in question.sliders:
				if "slider" + str(question.id) in request.form:
					slider_result = SliderResult(result.id, slider.id, int(request.form["slider" + str(question.id)]))
					db.session().add(slider_result)
					db.session().commit()
		elif question.question_type == "multichoice":
			for option in question.options:
				if "choice" + str(question.id) in request.form and int(request.form["choice" + str(question.id)]) == option.id:
					option_result = OptionResult(result.id, option.id)
					db.session().add(option_result)
					db.session().commit()

	return redirect("/result/" + str(result.id) + "/")

@app.route("/<poll_id>/", methods = ["GET", "POST"])
def handle_poll(poll_id):
	poll = Poll.query.get(poll_id)
	questions = []
	question = poll.first_question
	while question:
		questions.append(Question.query.get(question))
		question = questions[-1].successor
	if request.method == "GET":
		return render_template("polls/poll.html", poll=poll, questions=questions)

	best_score = -1.
	best_result = None
	for result in poll.results:
		score = 0.
		
		for slider_result in result.slider_results:
			if "slider" + str(Slider.query.get(slider_result.slider_id).question_id) in request.form:
				score += 1. - pow(abs(slider_result.value - int(request.form["slider" + str(Slider.query.get(slider_result.slider_id).question_id)])) / 100, 2)
		for option_result in result.option_results:
			if "choice" + str(Option.query.get(option_result.option_id).question_id) in request.form and int(request.form["choice" + str(Option.query.get(option_result.option_id).question_id)]) == option_result.option_id:
				score += 1.
		print("RESULT: ", result.name, score, "\n"*10)
		if score > best_score:
			best_score = score
			best_result = result
	if best_result == None:
		return render_template("polls/no_results.html")
	return render_template("polls/result.html", result=best_result)

@app.route("/result/<result_id>/")
def get_result(result_id):
	return render_template("polls/result.html", result=Result.query.get(result_id))