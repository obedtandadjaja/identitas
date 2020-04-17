from app.config import settings
from app.models import UserModel

from app.db import base


def init_db(db_session):
    user = UserModel.get_by_email(db_session, settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        UserModel.create(
            db_session,
            {
                "email": settings.FIRST_SUPERUSER,
                "password": settings.FIRST_SUPERUSER_PASSWORD,
                "is_superuser": True,
            }
        )
