import json
import random
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Blueprint

# image till 5_1

#print("\n\nhttp://127.0.0.1:5000/scenario/\n\n")

app = Blueprint('scenario', __name__)

class UserManager:
    def __init__(self, db_path='user_data.db'):
        self.db_path = db_path
        self.create_user_table()

    def create_user_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    total_wins INTEGER DEFAULT 0,
                    total_losses INTEGER DEFAULT 0,
                    total_matches INTEGER DEFAULT 0,
                    win_percentage REAL DEFAULT 0.0,
                    current_score INTEGER DEFAULT 0,
                    last_played TEXT,
                    achievements TEXT DEFAULT '',
                    level INTEGER DEFAULT 1,
                    experience_points INTEGER DEFAULT 0,
                    badges_bronze INTEGER DEFAULT 0,
                    badges_silver INTEGER DEFAULT 0,
                    badges_gold INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def add_or_update_user(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                print(f"User '{username}' already exists. Updating data...\n")
                self.update_user_data(username)
            else:
                print(f"User '{username}' not found. Creating new user...\n")
                cursor.execute('''
                    INSERT INTO users (username, last_played) 
                    VALUES (?, ?)
                ''', (username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()

        self.update_user_data(username)

    def update_user_data(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET total_matches = total_matches + 1, 
                    last_played = ? 
                WHERE username = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
            conn.commit()

    def update_game_results(self, username, wins=0, losses=0, current_score=0):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT total_wins, total_losses, total_matches FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            total_wins = user[0] + wins
            total_losses = user[1] + losses
            total_matches = user[2]
            win_percentage = (total_wins / total_matches) * 100 if total_matches > 0 else 0.0

            cursor.execute('''
                UPDATE users 
                SET total_wins = ?, total_losses = ?, current_score = ?, win_percentage = ? 
                WHERE username = ?
            ''', (total_wins, total_losses, current_score, win_percentage, username))
            conn.commit()

    def display_user_data(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user:
                print(f"User Data: {user}")
            else:
                print(f"User '{username}' not found.")

    def add_badge(self, username, badge_type):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if badge_type == 'bronze':
                cursor.execute('UPDATE users SET badges_bronze = badges_bronze + 1 WHERE username = ?', (username,))
            elif badge_type == 'silver':
                cursor.execute('UPDATE users SET badges_silver = badges_silver + 1 WHERE username = ?', (username,))
            elif badge_type == 'gold':
                cursor.execute('UPDATE users SET badges_gold = badges_gold + 1 WHERE username = ?', (username,))

            conn.commit()

    def update_experience(self, username, experience_points):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET experience_points = experience_points + ? WHERE username = ?', (experience_points, username))
            conn.commit()

    def add_achievement(self, username, achievement):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT achievements FROM users WHERE username = ?', (username,))
            current_achievements = cursor.fetchone()[0]
            if current_achievements:
                updated_achievements = current_achievements + ',' + achievement
            else:
                updated_achievements = achievement
            cursor.execute('UPDATE users SET achievements = ? WHERE username = ?', (updated_achievements, username))
            conn.commit()



class CYOAGame:
    def __init__(self, scenarios_file='scenario.json', user_manager=None):
        self.user_name = "aditya"
        self.scenarios_file = scenarios_file
        self.scenarios = self.load_scenarios()
        self.points = 50
        self.current_scenario = "stage1"
        self.rounds = 0
        self.user_manager = user_manager
        self.user_name = ""
        self.win = False
        self.user_manager.add_or_update_user(self.user_name)
        self.result = None

    def load_scenarios(self):
        with open(self.scenarios_file, 'r', encoding='utf-8') as file:
            return json.load(file)["scenarios"]

    def update_achievements_and_badges(self):
        print("Updating achievements, badges, and experience...")
        experience_points = self.points
        self.user_manager.update_experience(self.user_name, experience_points)

        if self.win:
            if self.points >= 100:
                self.user_manager.add_badge(self.user_name, 'gold')
            elif self.points >= 70:
                self.user_manager.add_badge(self.user_name, 'silver')
            elif self.points >= 50:
                self.user_manager.add_badge(self.user_name, 'bronze')
            if self.points < 20:
                self.user_manager.add_achievement(self.user_name, "Lucky")
            if self.points == 100:
                self.user_manager.add_achievement(self.user_name, "Perfectionist")
            if self.points == 50:
                self.user_manager.add_achievement(self.user_name, "Neutralist")

    

@app.route('/scenario/')
def index():
    global manager, cyoagame
    manager = UserManager()  
    cyoagame = CYOAGame(user_manager=manager)
    return render_template('scenario_index.html')

@app.route('/scenario/game/<scenario>', methods=['GET', 'POST'])
def game(scenario):
    scenario = cyoagame.scenarios[cyoagame.current_scenario]
    scenario['image_url'] = url_for('static', filename=f'scenario_images/{scenario["image_url"]}')
    if request.method == 'POST':
        choice = request.form.get('option')
        cyoagame.rounds += 1
        cyoagame.points += scenario['options'][choice]['point']
        cyoagame.current_scenario = scenario['options'][choice]['next']
        if cyoagame.current_scenario == 'end' or cyoagame.points >= 100 or cyoagame.points <= 0:
            return redirect(url_for('scenario.end_game', points=cyoagame.points))
        return redirect(url_for('scenario.game', scenario=cyoagame.current_scenario, points=cyoagame.points))
    return render_template('scenario_game.html', scenario=scenario, points=request.args.get('points', 50))


@app.route('/scenario/end')
def end_game():
    cyoagame.win = False
    points = int(request.args.get('points'))
    if points >= 100:
        cyoagame.result = f"You won the case!\nPoints:{points}"
        cyoagame.win = True
    elif points <= 0:
        cyoagame.result = f"You lost the case!\nPoints:{points}"
    else:
        if random.randint(1, 100) <= points:
            cyoagame.win = True
            cyoagame.result = f"cyoagame over, you WON!\nYour final score is {points}%."
        else:
            cyoagame.result = f"cyoagame over, you lost!\nYour final score is {points}%."
    if cyoagame.user_manager:
        cyoagame.user_manager.update_game_results(cyoagame.user_name, wins=(1 if cyoagame.win else 0), losses=(1 if not cyoagame.win else 0), current_score=cyoagame.points)
        cyoagame.update_achievements_and_badges()
    return render_template('scenario_end.html', result=cyoagame.result)


#app.run(debug=False)

