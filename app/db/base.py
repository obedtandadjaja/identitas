# Import all the models, so that base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User
