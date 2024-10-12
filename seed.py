from app import app
from models import db, Episode, Guest, Appearance
from datetime import datetime

def seed_data():
    with app.app_context():
        print("Clearing database...")
        try:
            db.session.query(Appearance).delete()
            db.session.query(Guest).delete()
            db.session.query(Episode).delete()
            db.session.commit()

            db.create_all()

            # Use datetime for date fields
            episode1 = Episode(date=datetime.strptime("1/11/1999", "%m/%d/%Y"), number=1)
            episode2 = Episode(date=datetime.strptime("1/12/1999", "%m/%d/%Y"), number=2)

            guest1 = Guest(name="Michael J. Fox", occupation="actor")
            guest2 = Guest(name="Sandra Bernhard", occupation="comedian")

            appearance1 = Appearance(rating=4, guest=guest1, episode=episode1)
            appearance2 = Appearance(rating=5, guest=guest2, episode=episode2)

            db.session.add_all([episode1, episode2, guest1, guest2, appearance1, appearance2])
            db.session.commit()
            print("Seeding completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

if __name__ == "__main__":
    seed_data()
