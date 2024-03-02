from flask import Flask

from controllers.recommendation_controller import recommendation_bp

app = Flask(__name__)

app.register_blueprint(recommendation_bp, url_prefix='/recommendations')

if __name__ == '__main__':
  app.run(debug=True)