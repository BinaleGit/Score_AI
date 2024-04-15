from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)


@app.route('/music')
def music():
    # Read the CSV file
    music_data = pd.read_csv('music.csv')
    # Convert the DataFrame to HTML table
    music_table = music_data.to_html()
    # Render the template with the HTML table
    return render_template('music.html', music_table=music_table)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        age = float(request.form.get('age'))  # Convert age to float
        # Prepare 2 groups (features, output)
        music_dt = pd.read_csv('music.csv')
        X = music_dt.drop(columns=['Scores'])  # Sample features (age, gender)
        Y = music_dt['Scores']  # Sample output
        model = DecisionTreeClassifier()
        model.fit(X, Y)  # Load features and sample data
        age_input = [[age]]  # Reshape age to a 2D array
        predictions = model.predict(age_input)  # Make prediction based on the input
        return render_template('predict.html', predictions=predictions)
    else:
        return render_template('predict.html')


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if request.method == 'POST':
        age = request.form.get('age') # X
        genre = request.form.get('genre') # y
        # update CSV with new data
        # Define the data for the new row
        new_row = {'Hours': age, 'Scores': genre}

        # Read the existing CSV file into a DataFrame
        music_dt = pd.read_csv('music.csv')

        # Append the new row to the DataFrame
        music_dt = music_dt._append(new_row, ignore_index=True)

        # Write the DataFrame back to the CSV file
        music_dt.to_csv('music.csv', index=False)
        
        # learn
        # Read the CSV file
        music_dt = pd.read_csv('music.csv')
        
        # prepare 2 groups (features, output)
        X = music_dt.drop(columns=['Scores'])  # Sample features (age, gender)
        Y = music_dt['Scores']  # Sample output
        model = DecisionTreeClassifier()
        model.fit(X, Y)  # Load features and sample data
        age_input = [[age]]  # Reshape age to a 2D array
        predictions = model.predict(age_input)  # Make prediction based on the input
        return render_template('predict.html', predictions=predictions)
    else:
        return render_template('learn.html') 


if __name__ == '__main__':
    app.run(debug=True)