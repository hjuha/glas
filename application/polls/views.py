from flask import render_template, request, redirect, url_for

from application import app, db
from application.polls.models import Poll, Question, Slider, Option

import hashlib

@app.route("/new/", methods = ["GET", "POST"])
def new_poll():
	if request.method == "GET":
		return render_template("polls/new.html")

	#print(request.form)

	#if hashlib.sha256(password.encode('utf-8')).hexdigest() != "c6d37d0e5d3d7445293322dd693bfb98d38ee3d7228e1628c2e85bf537abe880":
	#	return render_template("poems/new.html", form = form)

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
				#print("SLIDER", question, slider_left, slider_right)
			else:
				for key_ in request.form:
					if key_[:7+len(q_id)] == "option" + q_id + "_":
						options[-1].append(request.form[key_])
				#print("MULTICHOICE", question, options)

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


@app.route("/<poll_id>/")
def get_poll(poll_id):
	return render_template("polls/poll.html", poll = Poll.query.get(poll_id))