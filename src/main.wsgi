import os
import sys

activate_this = "/home/websites/flask/web-activity-logger/.venv/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))
sys.path.insert(0, "/home/websites/flask/web-activity-logger/src")
os.environ["FLASK_APP"] = "app.py"
os.environ["PYTHONPATH"] = "/home/websites/flask/webpage/src/web-activity-logger"
from activity_logger import create_app  # noqa: E402, E261

application = create_app()
