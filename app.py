from flask import Flask, render_template
from config import Config
from extensions import db
from flask_migrate import Migrate
from routes import main
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_resources(app)
    register_extensions(app)
    register_session(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    
def register_resources(app):    
    app.register_blueprint(main)
    
def register_session(app):
    Session(app)
    
app = create_app()    

if __name__ == '__main__':
    app.run(debug=True, port=5001) 