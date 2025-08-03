from app import db, app
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated!")

    user = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()
    print("✅ Admin user created!")
