from activity_logger.models.db_activites import init_activities
from activity_logger.models.org import init_user


def build_default_database():
    init_activities()
    init_user()
