from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Home Route
class Home(Resource):
    def get(self):
        return jsonify({"message": "Welcome to the Late Show"})

# Episode Resource
class EpisodeResource(Resource):
    def get(self, id=None):
        if id:
            episode = Episode.query.get(id)
            if episode:
                return jsonify(episode.to_dict(include_appearances=True))
            return jsonify({"error": "Episode not found"}), 404
        else:
            episodes = Episode.query.all()
            return jsonify([episode.to_dict() for episode in episodes])

# Guest Resource
class GuestResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return jsonify([guest.to_dict() for guest in guests])

class AppearanceResource(Resource):
    def post(self):
        data = request.get_json()

        # Validate that required keys are present
        if 'guest_id' not in data or 'episode_id' not in data or 'rating' not in data:
            return make_response(jsonify({"errors": ["guest_id, episode_id, and rating are required"]}), 400)

        # Check if the guest and episode exist
        guest = Guest.query.get(data.get('guest_id'))
        episode = Episode.query.get(data.get('episode_id'))

        if not guest:
            return make_response(jsonify({"errors": ["Guest not found"]}), 404)

        if not episode:
            return make_response(jsonify({"errors": ["Episode not found"]}), 404)

        # Check if the Appearance already exists
        existing_appearance = Appearance.query.filter_by(
            guest_id=data['guest_id'], episode_id=data['episode_id']
        ).first()

        if existing_appearance:
            return make_response(jsonify({"errors": ["This appearance already exists"]}), 400)

        # Create a new Appearance with validation
        try:
            new_appearance = Appearance(
                rating=data['rating'],
                guest_id=data['guest_id'],
                episode_id=data['episode_id']
            )
            db.session.add(new_appearance)
            db.session.commit()

            # Prepare response data
            response_data = {
                "id": new_appearance.id,
                "rating": new_appearance.rating,
                "guest_id": new_appearance.guest_id,
                "episode_id": new_appearance.episode_id,
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                },
                "episode": {
                    "id": episode.id,
                    "number": episode.number,
                    "date": episode.date.strftime('%m/%d/%y')
                }
            }

            return make_response(jsonify(response_data), 201)

        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"errors": ["Failed to create appearance: " + str(e)]}), 500)


# Register Resources
api.add_resource(Home, '/')
api.add_resource(EpisodeResource, '/episodes', '/episodes/<int:id>')
api.add_resource(GuestResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')

if __name__ == '__main__':
    app.run(debug=True)
