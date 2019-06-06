import os
from validate_email import validate_email

from flask import Flask, request, abort, make_response, jsonify
import logging

from user import User
from users_legacy_repository import check_fiscal_code
from users_repository import UserDAO, UserRepositoryException

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
def health_check():
    return '', 200


@app.route('/user_management/api/v1.0/users/<string:username>/<string:password>', methods=['GET'])
def get_user(username, password):
    """
        This function exports the url used to send a login request.
        The content of request is url-encoded and contains username and password
    :param username: inserted username
    :param password: inserted password
    """

    # Check format of the request, responding with HTTP Bad Request in case of failed validation.
    if not is_suitable_parameter(username) or not is_suitable_parameter(password):
        abort(400)

    # Check if the user with the given username and password exists in the datastore
    user = UserDAO.find_user_by_username_and_password(username, password)
    if user is None:
        abort(404)  # Not found
    user_dict = user.to_dict()
    return jsonify({'user': user_dict}), 200  # Found


@app.route('/user_management/api/v1.0/users', methods=['POST'])
def register_user():
    """
        This function exports the url used to send a registration request.
        The content of the request is a json array containing the following information:
        username, password, name, surname, fiscal code.
        The username is used as key in the registration process.
        The fiscal code is used to verify that the user is authorized to use the service.
    """

    # Check format of the request, responding with HTTP Bad Request in case of failed validation.
    if not request.json:
        abort(400)
    if 'username' not in request.json or not (is_suitable_parameter(request.json['username'])):
        abort(400)
    if 'password' not in request.json or not (is_suitable_parameter(request.json['password'])):
        abort(400)
    if 'name' not in request.json or not (is_suitable_parameter(request.json['name'])) \
            or not request.json['name'].isalpha():
        abort(400)
    if 'surname' not in request.json or not (is_suitable_parameter(request.json['surname'])) \
            or not request.json['surname'].isalpha():
        abort(400)
    if 'fiscalCode' not in request.json or not (is_suitable_parameter(request.json['fiscalCode'])):
        abort(400)
    if 'mail' not in request.json or not (is_valid_mail(request.json['mail'])):
        abort(400)

    # Check if the user is authorized to sign up
    user_type = check_fiscal_code(request.json['fiscalCode'])
    if user_type is None:
        abort(403)  # Access denied
    else:
        user = User()
        user.name = request.json['name']
        user.surname = request.json['surname']
        user.username = request.json['username']
        user.password = request.json['password']
        user.type = user_type
        user.mail = request.json['mail']
        try:
            inserted = UserDAO.add_user(user)
            if not inserted:
                abort(409)  # The provided username already exists
            user_dict = user.to_dict()
            return jsonify({'user': user_dict}), 201  # Created

        except UserRepositoryException:
            logger.error('Exception occurred while accessing Users Data', exc_info=True)
            abort(500)  # Internal Server Error


@app.errorhandler(400)
def bad_request(error):
    logger.error(error)
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    logger.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(409)
def conflict(error):
    logger.error(error)
    return make_response(jsonify({'error': 'Conflict - Username already exists'}), 409)


@app.errorhandler(403)
def unauthorized_registration(error):
    logger.error(error)
    return make_response(jsonify({'error': 'Unauthorized registration'}), 403)


@app.errorhandler(500)
def internal_server_error(error):
    logger.error(error)
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)


def is_valid_mail(mail_string):
    return validate_email(mail_string)


def is_suitable_parameter(parameter):
    #  Checks if the parameter is a not-empty string and has not blank spaces.
    s = parameter.replace(" ", "").replace("\t", "").replace("\n", "")
    if s == "" or s != parameter:
        return False
    else:
        return True


if __name__ == '__main__':
    host = os.getenv('LISTEN_IP', '0.0.0.0')
    port = int(os.getenv('LISTEN_PORT', '80'))
    app.run(host=host, port=port, threaded=True)
