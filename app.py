from flask import Flask
from dotenv import load_dotenv

from controllers.recommendation_controller import recommendation_bp
from controllers.event_controller import event_bp
from controllers.category_controller import category_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(recommendation_bp, url_prefix='/recommendations')
app.register_blueprint(event_bp, url_prefix='/events')
app.register_blueprint(category_bp, url_prefix='/categories')

if __name__ == '__main__':
  app.run(debug=True)
