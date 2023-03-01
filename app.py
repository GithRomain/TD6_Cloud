from flask import Flask
from pymongo import MongoClient

# Create a Flask application instance
app = Flask(__name__)

# Connect the database
client = MongoClient("mongodb://mongodb:27017/")

db = client.td6db

collection = db.td6_collection

app = Flask(__name__)

# Insert data in mongodb
documents = [{"name": "Jane Doe", "age": 25}, {"name": "Jim Smith", "age": 35}]
collection.insert_many(documents)

@app.route('/')
def hello():
    # Fetch all document from the test_collection
    data = list(collection.find({}))
    with open('file.txt', 'r') as f:
        content = f.read()
#    return content
    return str(data) + "\n" + content

# Start the Flask application if this file is being executed as the main script
if __name__ == "__main__":
    # Start the Flask application, listening on all available interfaces
    app.run(debug=True, host="0.0.0.0")