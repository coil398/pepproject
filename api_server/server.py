from flask import Flask, request, jsonify, abort, make_response


api = Flask(__name__)

@api.route('/target/get/<string:num>', methods=['GET'])
def get_data(num):
    data = num
    print(data)
    result = {'result': 'OK',
                'data': data
    }
    return make_response(jsonify(result))


@api.route('/target/post', methods=['POST'])
def post_data():
    data = request.form
    result = {'result': 'OK',
                'data': data
    }
    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)
