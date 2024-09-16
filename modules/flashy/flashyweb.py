"""
This module contains a Flask web application for a flashy quiz game.
The main functionalities of this application include:
- Displaying random quiz questions from a CSV file
- Allowing users to submit their answers
- Keeping track of the user's score
Functions:
- new_card: Generates a new quiz card with a random question and shuffled answer options.
- flashy: Renders the flashy.html template with the current quiz question and answer options.
- submit: Handles the user's answer submission and updates the score.
Global Variables:
- score_value: An integer representing the user's current score.
- current_card: A dictionary representing the current quiz question.
- current_list: A list of shuffled answer options for the current quiz question.
- leaderboard: A dictionary storing player names and their scores.
Routes:
- /flashy: Renders the flashy.html template with the current quiz question and answer options.
- /flashy/submit: Handles the user's answer submission and redirects to the /flashy route.
- /flashy/set_name: Sets the player name and redirects to the /flashy route.
Note: This module requires the Flask, pandas, and json libraries to be installed.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, Blueprint
import random
import pandas as pd
import json
import os

questions_csv = "modules/flashy/questions.csv"
leaderboard_json = "modules/flashy/leaderboard.json"

app = Blueprint('flashyweb', __name__)
app.secret_key = 'samatva'

score_value = 0
current_card = {}
current_list = []
leaderboard = {}

try:
    data_to_display = pd.read_csv(questions_csv)
    oriented_data = data_to_display.to_dict(orient="records")
except FileNotFoundError:
    oriented_data = []

def load_leaderboard():
    global leaderboard
    try:
        with open(leaderboard_json, 'r') as f:
            content = f.read().strip()
            if content:
                leaderboard = json.loads(content)
            else:
                leaderboard = {}
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}
    
    # Ensure leaderboard is always a dictionary
    if not isinstance(leaderboard, dict):
        leaderboard = {}

def save_leaderboard():
    with open(leaderboard_json, 'w') as f:
        json.dump(leaderboard, f)

# Add this function to initialize the leaderboard file if it doesn't exist
def initialize_leaderboard():
    if not os.path.exists(leaderboard_json):
        with open(leaderboard_json, 'w') as f:
            json.dump({}, f)

# Call this function at the start of your application
initialize_leaderboard()

def new_card():
    """
    Generates a new flashcard with a random question and a shuffled list of answer options.
    Returns:
        current_card (str): The randomly chosen question for the flashcard.
        shuffle_list (list): The shuffled list of answer options for the flashcard.
    """
    global current_card, current_list
    current_card = random.choice(oriented_data)
    shuffle_list = ["Wrong Answer 1", "Wrong Answer 2", "Correct Answer", "Wrong Answer 3"]
    random.shuffle(shuffle_list)
    current_list = shuffle_list
    return current_card, shuffle_list

@app.route('/')
def flashy():
    """
    Function to generate a new flashcard and render the flashy.html template.
    Returns:
        str: The question of the current flashcard.
        list: The options for the current flashcard.
        int: The current score value.
    """
    global score_value, current_card, current_list, leaderboard
    current_card, shuffle_list = new_card()
    load_leaderboard()
    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:15])
    player_name = session.get('player_name', '')  # Get the player name from the session
    
    messages = session.pop('flashmsg', '')  # Get and remove the flash message from the session
    
    return render_template('flashy.html', 
                           question=current_card["Question"], 
                           options=[current_card[opt] for opt in shuffle_list], 
                           score=score_value, 
                           leaderboard=sorted_leaderboard,
                           player_name=player_name,
                           enumerate=enumerate,
                           messages=messages)  # Pass messages to the template

@app.route('/set_name', methods=['POST'])
def set_name():
    player_name = request.form.get('player_name', '').strip()
    session['player_name'] = player_name
    return redirect(url_for('flashyweb.flashy'))  # Change this line

@app.route('/submit', methods=['POST'])
def submit():
    """
    Submits the user's choice and updates the score.
    Returns:
        - If 'Correct Answer' key is not found in the current question data, returns an error message and status code 500.
        - Otherwise, updates the score if the selected option matches the correct answer.
        - Retrieves a new card and shuffles the list.
        - Redirects to the 'flashy' route.
    """
    global score_value, current_card, current_list, leaderboard

    selected_option = request.form['choice']
    player_name = request.form.get('player_name', '').strip()
    
    if not player_name:
        player_name = session.get('player_name', '')
    
    correct_answer = current_card.get("Correct Answer")
    
    if not correct_answer:
        # Log the error and generate a new card
        print(f"Error: 'Correct Answer' key not found in the current question data: {current_card}")
        session['flashmsg'] = "An error occurred. Moving to the next question."
        current_card, shuffle_list = new_card()
        return redirect(url_for('flashyweb.flashy'))
    
    if selected_option == correct_answer:
        score_value += 1
        session['flashmsg'] = ''
        if player_name:
            if player_name not in leaderboard or score_value > leaderboard[player_name]:
                leaderboard[player_name] = score_value
                save_leaderboard()
    else:
        session['flashmsg'] = f"Wrong Answer! The correct answer was: {correct_answer}"

    current_card, shuffle_list = new_card()
    return redirect(url_for('flashyweb.flashy'))  # Change this line

# Run the app by integrating it with your existing Flask app
