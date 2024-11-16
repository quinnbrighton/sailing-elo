import pandas as pd
from app import db, app
from app import Skipper

def load_data():
    skippers = pd.read_csv('data/skippers.csv')

    for _, row in skippers.iterrows():
        # Check if the skipper already exists in the database
        existing_skipper = Skipper.query.filter_by(name=row['name']).first()
        if existing_skipper is None:
            #print(f"Inserting new skipper: {row['name']}")
            db.session.add(Skipper(
                id=row['id'],
                name=row['name'],
                position=row['position'],
                year=row['year'],
                adjusted_estimate=row['Adjusted Estimate'],
                std_error=row['Std. Error'],
                z_value=row['z value'],
                p_value=row['Pr(>|z|)'],
                school_name=row['School Name'],
                image_token=row['Image Token'],
                school_token=row['School Token'],
                rating=row['Rating']
            ))
        else:
            print(f"Skipping existing skipper: {row['name']}")

    db.session.commit()


# Initialize the database
with app.app_context():
    db.drop_all()  # Optionally drop all tables (be careful with this!)
    db.create_all()  # Create tables defined in models

if __name__ == "__main__":
    with app.app_context():
        load_data()  # Call the function to load the data