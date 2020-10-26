from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from api.face_detection.route import face_detection


def create_app():
    app = app = Flask(__name__)

    CORS(app)

    app.config['SWAGGER'] = {
        'title': 'Flask Face Detection api',
        'uiversion': 3
    }

    app.config['SWAGGER']['openapi'] = '3.0.2'

    Swagger(app)

    app.register_blueprint(face_detection, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port, debug=True)
