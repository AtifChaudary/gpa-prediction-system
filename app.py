# import libraries
from flask import Flask, request, render_template
import pickle

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

    final_inputs = [[int(x) for x in request.form.values()]]
    prediction = model.predict(final_inputs)

    output = round(prediction[0], 2)

    return render_template('index.html', predicted_result='Student GPA Will be  {}'.format(output),matricmarks=request.form['matricmarks'],fscmarks=request.form['fscmarks'],output=output)

if __name__ == "__main__":
    app.run(debug=True)
