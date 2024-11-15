def load_data():
    #races = pd.read_csv('data/races.csv')
    #venues = pd.read_csv('data/venues.csv')
    skippers = pd.read_csv('data/skippers.csv')
    #weather = pd.read_csv('data/weather.csv')

    #for _, row in races.iterrows():
    #    db.session.add(Race(name=row['name'], date=row['date'], location=row['location'], 
    #                        wind_speed=row['wind_speed'], wind_direction=row['wind_direction']))

    for _, row in skippers.iterrows():
        db.session.add(Skipper(
            id=row['id'],
            name=row['name'],
            position=row['position'],
            year=row['year'],
            adjusted_estimate=row['Adjusted Estimate'],
            std_error=row['Std. Error'],
            z_value=row['z value'],
            p_value=row['Pr(>|z|)']
        ))

#    for _, row in venues.iterrows():
#        db.session.add(Venue(name=row['name'], location=row['location']))

#    for _, row in weather.iterrows():
#        db.session.add(Weather(venue_id=row['venue_id'], wind_speed=row['wind_speed'], 
#                               wind_direction=row['wind_direction']))

    db.session.commit()