# import libraries
from flask import Flask, request, render_template
import pandas as pd
import pickle
from sklearn import preprocessing
from flask_mysqldb import MySQL
import numpy as np

# create app and load the trained Model
app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql12388141'
app.config['MYSQL_PASSWORD'] = 'G3NfUsfXUG'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12388141'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL()
mysql.init_app(app)

model = pickle.load(open('Trained_Model.pkl', 'rb'))



# Route to handle Feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/feedback',methods=['POST'])
def feedback_save():
    fid = np.random.randint(100)
    name=request.form['name']
    actualGPA=request.form['actualGPA']
    email=request.form['email']
    message=request.form['message']
    cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE feedback (id INTEGER,name VARCHAR(50),actualGPA VARCHAR(50),email VARCHAR(50),feedback VARCHAR(150))''')   
    cur.execute('''INSERT INTO feedback VALUES (%s,%s,%s,%s,%s)''',(fid,name,actualGPA,email,message))
    mysql.connection.commit()
    return render_template('feedback_submitted.html')

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
