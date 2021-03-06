
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
#    app = Flask(__name__,static_folder='../../frontend/dist')
    app = Flask(__name__,static_folder='../frontend_dist')

    app.debug = debug
    # secret key for sessions
    app.config['SECRET_KEY'] = 'pippo!'

    from .apirouter import apirouter
    app.register_blueprint(apirouter,url_prefix="/api")

    socketio.init_app(app,async_mode='threading')

    @app.route('/')
    def index():
        return app.send_static_file("index.html")

    @app.route('/static/<path:path>')
    def dist_static(path):
        print(path)
        return send_from_directory("../frontend_dist/static", path)

    return app
