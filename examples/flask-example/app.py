from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/merge', methods=['POST', 'GET'])
def merge_topics():
    topic1 = request.args.get('topic1')
    topic2 = request.args.get('topic2')
    if topic1 == None or topic2 == None:
    	raise InvalidUsage('provide both topic1 and topic2')
    return "merging " + topic1 + " " + topic2

@app.route('/split', methods=['POST', 'GET'])
def split_topics():
    topic1 = request.args.get('topic1')
    topic2 = request.args.get('topic2')
    if topic1 == None or topic2 == None:
    	raise InvalidUsage('provide both topic1 and topic2')
    return "spliting " + topic1 + " " + topic2

# Start a development server
if __name__ == '__main__':
    app.run(debug=True)