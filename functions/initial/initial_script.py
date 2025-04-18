from functions.database.database_alc import User, db_session, Servers

def initial_script():
    # Check if an admin user exists
    existing_admin = db_session.query(User).filter_by(name="isma").first()

    if not existing_admin:
        # Create an admin user if none exists
        new_user = User(name="isma", is_admin=True, password="smktarat")
        db_session.add(new_user)
        db_session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    # turn off all servers
    servers = db_session.query(Servers).filter(Servers.status == True).all()

    for server in servers:
        db_session.query(Servers).filter_by(id=server.id).update({"status": False})

    db_session.commit()
    db_session.close()
