from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def show_survey():
    """ Show the survey"""
    return render_template("survey_page.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """ Redirect to first question"""
    # Clear responses
    session["responses"] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def answer_question():
    """ Get answers and go to next question"""

    # Get the answer
    choice = request.form['answer']

    # Add answer to responses
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    # Check if survey continues or ends
    if (len(responses) == len(survey.questions)):
            return redirect("/end")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:question_number>")
def display_question(question_number):
    """ Display question """
    responses = session["responses"]

    if(responses is None):
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        return redirect("/end")
    elif(len(responses) != question_number):
        # If user attempts to access questions out of order
        flash(f"Invalid question: {question_number}!")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[question_number]
    return render_template("questions.html", question_number=question_number, question=question)

@app.route("/end")
def end_survey():
    """ End Survey """
    return render_template("end.html")