# import libraries
from flask import Flask, request, render_template
import pandas as pd
import pickle
from sklearn import preprocessing

# create app and load the trained Model
app = Flask(__name__)
model = pickle.load(open('Trained_Model.pkl', 'rb'))

# Route to handle HOME
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle PREDICTED RESULT
@app.route('/',methods=['POST'])
def predict():

    matricmarks=request.form['matricmarks']
    fscmarks=request.form['fscmarks']
    uniName=request.form['uniName']

    user_input = pd.DataFrame({ 'Matric Marks': [matricmarks],'FSC Marks': [fscmarks],'University Name': [uniName]})
    le = preprocessing.LabelEncoder()
    user_input['University Name'] = le.fit_transform(user_input['University Name'])
    prediction = model.predict(user_input)

    output = round(prediction[0], 2)

    return render_template('index.html', predicted_result='Student GPA Will be  {}'.format(output),matricmarks=request.form['matricmarks'],fscmarks=request.form['fscmarks'],uniName=request.form['uniName'],output=output)

if __name__ == "__main__":
    app.run(debug=True)
