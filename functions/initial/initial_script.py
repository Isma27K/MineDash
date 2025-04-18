from functions.database.database_alc import User, db_session

def initial_script():
    # Check if an admin user exists
    existing_admin = db_session.query(User).filter_by(name="imAdmin").first()

    if not existing_admin:
        # Create an admin user if none exists
        new_user = User(name="imAdmin", is_admin=True, password="smktarat")
        db_session.add(new_user)
        db_session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
