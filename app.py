from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Create Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Connect to a database. Will create one if not already available.
db = mongo.db.mars_db

# List of dictionaries
dogs = [{"name": "Fido", "type": "Lab"},
        {"name": "Rex", "type": "Collie"},
        {"name": "Suzzy", "type": "Terrier"},
        {"name": "Tomato", "type": "Retriever"}]


# create route that renders index.html template
@app.route("/")
def index():
        mars_data = mongo.db.collection.find_one()
        return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

        mars_data = scrape_mars.scrape()
        mongo.db.collection.update({}, mars_data, upsert=True)
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
