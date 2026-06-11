from backend.database.base import Base
from backend.database.connection import engine

# Import ORM models
from backend.models.user import User

Base.metadata.create_all(bind=engine)

print("? Database initialized successfully.")
