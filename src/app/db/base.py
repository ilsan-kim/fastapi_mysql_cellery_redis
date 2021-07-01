# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.user import User  # noqa
from app.models.timetable import Lesson # noqa
