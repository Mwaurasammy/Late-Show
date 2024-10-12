from app import app
from models import db, Episode, Guest, Appearance
from datetime import datetime
from sqlalchemy import text

def reset_sequences():
    with app.app_context():
        # Reset the sequences for each table
        db.session.execute(text("ALTER SEQUENCE appearance_id_seq RESTART WITH 1"))
        db.session.execute(text("ALTER SEQUENCE guest_id_seq RESTART WITH 1"))
        db.session.execute(text("ALTER SEQUENCE episode_id_seq RESTART WITH 1"))
        db.session.commit()

def seed_data():
    with app.app_context():
        print("Clearing database...")
        try:
            # Delete all existing entries from the tables
            db.session.query(Appearance).delete()
            db.session.query(Guest).delete()
            db.session.query(Episode).delete()
            db.session.commit()  # Commit changes to remove entries
            
            # Create all tables again to reset the schema
            db.create_all()

            # Reset sequences to start IDs from 1
            reset_sequences()

            # Use datetime for date fields
            episode1 = Episode(date=datetime.strptime("1/11/1999", "%m/%d/%Y"), number=1)
            episode2 = Episode(date=datetime.strptime("1/12/1999", "%m/%d/%Y"), number=2)
            episode3 = Episode(date=datetime.strptime("1/12/2000", "%m/%d/%Y"), number=3)

            guest1 = Guest(name="Michael J. Fox", occupation="actor")
            guest2 = Guest(name="Sandra Bernhard", occupation="comedian")
            guest3 = Guest(name="Christiano Ronaldo", occupation="footballer")

            appearance1 = Appearance(rating=4, guest=guest1, episode=episode1)
            appearance2 = Appearance(rating=5, guest=guest2, episode=episode2)

            # Add all records to the session
            db.session.add_all([episode1, episode2, episode3, guest1, guest2, guest3, appearance1, appearance2])
            db.session.commit()  # Commit changes to save new entries
            
            print("Seeding completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

if __name__ == "__main__":
    seed_data()
