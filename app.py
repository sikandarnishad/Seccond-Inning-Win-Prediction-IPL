<<<<<<< HEAD
from flask import Flask, render_template, request, send_from_directory

import pickle
import pandas as pd

app = Flask(__name__)

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html', teams=teams, cities=cities)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/predict', methods=['POST'])
def predict():
    batting_team = request.form['batting_team']
    bowling_team = request.form['bowling_team']
    selected_city = request.form['selected_city']
    target = int(request.form['target'])
    score = int(request.form['score'])
    overs = int(request.form['overs'])
    wickets = int(request.form['wickets'])

    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    return render_template('index.html', teams=teams, cities=cities, result={'batting_team': batting_team, 'win_probability': round(win*100), 'bowling_team': bowling_team, 'loss_probability': round(loss*100)})

if __name__ == '__main__':
    app.run(debug=True)
=======
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPL Win Predictor</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <style>
        .form-container {
            max-width: 400px;
            margin: auto;
        }
        .form-group {
            margin-bottom: 15px; /* Increased margin for more spacing */
        }
        
        label {
            font-weight: bold;
            color:blue;
            font-size: 25px; /* Increased font size */
        }
    </style>
    

</head>
<body>
<h1 style="font-size:40px;text-align: center;color:black; margin: 10px;">Second Inning Win Pridiction</h1>
<div style="background-image: url('https://resources.pulse.icc-cricket.com/photo-resources/2020/10/31/360fea86-e3f3-42f1-8ada-6fc1d82dd4c7/GettyImages-625462058.jpg?width=1920&height=1080');
background-size: cover; height:500px; padding-top: 150px; text-align: center;">
  
  <form action="/predict" method="post">

    
    <div class="form-group">
        <label for="batting_team">Select the batting team:</label>
        <select name="batting_team" id="batting_team">
            {% for team in teams %}
                <option value="{{ team }}">{{ team }}</option>
            {% endfor %}
        </select>
    </div>
    <div class="form-group">
        <label for="bowling_team">Select the bowling team:</label>
        <select name="bowling_team" id="bowling_team">
            {% for team in teams %}
                <option value="{{ team }}">{{ team }}</option>
            {% endfor %}
        </select>
    </div>


    <div class="form-group">
        <label for="selected_city">Select host city:</label>
        <select name="selected_city" id="selected_city">
            {% for city in cities %}
                <option value="{{ city }}">{{ city }}</option>
            {% endfor %}
        </select>
    </div>

    <div class="form-group">
        <label for="target">Target:</label>
        <input type="number" name="target" id="target" required>
    </div>

    <div class="form-group">
        <label for="score">Score:</label>
        <input type="number" name="score" id="score" required>
    </div>

    <div class="form-group">
        <label for="overs">Overs completed:</label>
        <input type="number" name="overs" id="overs" required>
    </div>

    <div class="form-group">
        <label for="wickets">Wickets out:</label>
        <input type="number" name="wickets" id="wickets" required>
    </div>

    <div class="form-group">
        <input type="submit" value="Predict Probability">
    </div>
</form>
<!-- 
{% if result %}
        <h2>{{ result['batting_team'] }} - {{ result['win_probability'] }}%</h2>
        <h2>{{ result['bowling_team'] }} - {{ result['loss_probability'] }}%</h2>
    {% endif %}
    -->
    {% if result %}
    <h2 style="color: yellow;">{{ result['batting_team'] }} - {{ result['win_probability'] }}%</h2>
    <h2 style="color: yellow;">{{ result['bowling_team'] }} - {{ result['loss_probability'] }}%</h2>
{% endif %}

</div>
</body>
</html>
>>>>>>> 8c8302c71fde2c1d7c726a2a2a69491bb9a8776f
