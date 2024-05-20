from flask import Flask, jsonify, request, render_template 
from flask_sqlalchemy import SQLAlchemy  # for database interaction
from passcode import password as db_uri


app = Flask(__name__)  # create new Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable SQLAlchemy event system to save resources
db = SQLAlchemy(app)  # passing the Flask app to SQLAlchemy 

class NetflixTitle(db.Model):  # define model class for 'NetflixTitle'
    id = db.Column(db.Integer, primary_key=True)  # id will be the primary key column
    title = db.Column(db.String(100))
    type = db.Column(db.String(100))  
    country = db.Column(db.String(100))  
    release_year = db.Column(db.Integer)  

@app.route('/')  # root endpoint
def index():
    return render_template('movie_titles.html')  # retrieves the movie_titles.html template at the root URL

@app.route('/get_titles', methods=['GET'])  # get all titles displayed
def get_titles():
    titles = NetflixTitle.query.all()  # queries all records in NetflixTitle
    return jsonify([{'id': title.id, 'title': title.title, 'type': title.type, 'country': title.country, 'release_year': title.release_year} for title in titles])  # return JSON array of titles

@app.route('/get_title/<int:id>', methods=['GET'])  # get a single title by id
def get_title(id):
    title = NetflixTitle.query.get(id)  # retrieve a single title using its id
    if title:
        return jsonify({'id': title.id, 'title': title.title, 'type': title.type, 'country': title.country, 'release_year': title.release_year}), 200  # return JSON object of the title if found
    return jsonify({'error': 'Title not found'}), 404  

@app.route('/create_title', methods=['POST'])  # create a new title
def create_title():
    data = request.form  # get data from form submission
    new_title = NetflixTitle(title=data.get('title'), type=data.get('type'), country=data.get('country'), release_year=data.get('release_year')) 
    db.session.add(new_title) 
    db.session.commit()  
    return jsonify({'message': 'Title created successfully'}), 201

@app.route('/update_title/<int:id>', methods=['PUT'])  # update an existing title
def update_title(id):
    title = NetflixTitle.query.get(id)  # retrieve the title to be updated by id
    if title:
        data = request.form  # gets data from form submission
        title.title = data.get('title', title.title)  # sets new values or retains old if not provided - important!
        title.type = data.get('type', title.type)
        title.country = data.get('country', title.country)
        title.release_year = data.get('release_year', title.release_year)
        db.session.commit()  # commit changes to the database
        return jsonify({'message': 'Title updated successfully'}), 200
    else:
        return jsonify({'error': 'Title not found'}), 404  

@app.route('/delete_title/<int:id>', methods=['DELETE'])  
def delete_title(id):
    title = NetflixTitle.query.get(id)  
    if title:
        db.session.delete(title)
        db.session.commit()
        return jsonify({'message': 'Title deleted successfully'}), 200
    else:
        return jsonify({'error': 'Title not found'}), 404  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # to create all database tables
    app.run(debug=True)  # enable debug mode
