import sqlite3
from flask import request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Database Creation
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///city.db"

db = SQLAlchemy(app)

class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False, unique=True)
    country = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    
    #Convert data to dictionary to work with json
    def to_dict(self):
        return{
            "id" : self.id,
            "city" : self.city,
            "country" : self.country,
            "population" : self.population
        }
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"messege": "Welcome to City Population app"})

# @app.route("/upsert")
# def home():
#     return jsonify({"messege": "Welcome to City Population app"})



#Endpoint for cities
@app.route("/cities", methods=["GET"])
def get_cities():
    cities = Cities.query.all()
    
    return jsonify([city.to_dict() for city in cities])

#HealthCheck endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200


#Get city population info
@app.route("/cities/name/<string:city_name>", methods=["GET"])
def get_city(city_name):
    city = Cities.query.filter_by(city=city_name).first()
    if city:
        return jsonify(city.to_dict())
    else:
        return jsonify({"error": "City not found!"}), 404
    

#Add City to DB
@app.route("/cities", methods=["POST"])
def add_city():
    data = request.get_json()
    
    new_city = Cities(city=data["city"],
                                country=data["country"],
                                population=data['population'])
    db.session.add(new_city)
    db.session.commit()
    
    return jsonify(new_city.to_dict()), 201

#Update CITY

@app.route("/cities/<int:city_id>", methods=["PUT"])
def update_city(city_id):
    data = request.get_json()
    city = Cities.query.get(city_id)
    
    if city:
        city.city = data.get("city", city.city)
        city.country = data.get("country", city.country)
        city.population = data.get("population", city.population)
        
        db.session.commit()
        
        return jsonify(city.to_dict())
    else:
        return jsonify({"error": "City not found!"}), 404
    
#Delete city from list
    
@app.route("/cities/<int:city_id>",methods=["DELETE"])
def delete_city(city_id):
    city = Cities.query.get(city_id)
    if city:
        db.session.delete(city)
        db.session.commit()
        
        return jsonify({"message": "City was deleted"})
    else:
        return jsonify({"error": "City not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)