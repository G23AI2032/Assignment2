from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://34.68.37.200:27017/') 
 # Update with your MongoDB URI
db = client['contact_form']
collection = db['messages']

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Insert into MongoDB
    message_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'message': message
    }
    collection.insert_one(message_data)

    return 'Message recorded successfully'

# Route to display stored messages
@app.route('/messages')
def messages():
    # Retrieve all messages from MongoDB
    messages = list(collection.find({}, {'_id': 0}))

    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

