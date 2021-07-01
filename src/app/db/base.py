# Import all the models, so that Base has them before being
# imported by Alembic
from ..models.user import User  # noqa
from ..models.timetable import Lesson # noqa
