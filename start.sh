
gunicorn main:app -w 1 --log-file -

# AND MAIN py is From you main.py file
# and app is from THIS app = Flask(__name__)


# AND NOW DEPLOY TO GLICTH USING GITHUB