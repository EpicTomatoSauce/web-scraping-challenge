from flask import Flask, render_template, redirect
# https://flask-pymongo.readthedocs.io/en/latest/
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
  
    mars_data = mongo.db.mars_data
    mars_scrape = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_scrape, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)