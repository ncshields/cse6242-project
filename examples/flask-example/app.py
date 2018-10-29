from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

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

@app.route('/api/cluster-terms', methods=['POST'])
def post():
    """
    This is an api that consumes list of cluster terms
    Call this api passing `cluster_terms` lists of terms
    ---
    tags:
      - Consume lists of terms
    parameters:
      - name: cluster_terms
        in: body
        required: true
        description: Modified lists for terms
        schema:
          id: Cluter terms
          required:
            - cluster_terms
          properties:
            cluster_terms:
              type: array
              description: The new terms list.
              default: Empty list
              example: [["hello", "world"], ["new", "terms", "here"]]
    responses:
      400:
        description: Validation issue. cluster_terms was not provided
      500:
        description: Internal server error
      200:
        description: Post was successful
    """
    request_body = request.json
    if 'cluster_terms' not in request_body:
        raise InvalidUsage('provide a value for cluster_terms')

    cluster_terms = request_body['cluster_terms']
    return jsonify(cluster_terms)

@app.route('/api/merge', methods=['POST'])
def merge_topics():
	"""
    This is an api to merge two topics
    Call this api passing topic1 and topic2 as query params
    ---
    tags:
      - Merge Topics API
    parameters:
      - name: topic1
        in: query
        type: string
        required: true
        description: The first topic to merge
      - name: topic2
        in: query
        type: string
        required: true
        description: The second topic to merge
    responses:
      400:
        description: Validation issue. One or both topics were not provided
      500:
		description: Internal server error
      200:
        description: The two topics were merged
    """
	topic1 = request.args.get('topic1')
	topic2 = request.args.get('topic2')
	if topic1 == None or topic2 == None:
		raise InvalidUsage('provide both topic1 and topic2')
	return "merging " + topic1 + " " + topic2

@app.route('/api/split', methods=['POST'])
def split_topics():
	"""
    This is an api to split two topics
    Call this api passing topic1 and topic2 as query params
    ---
    tags:
      - Split Topics API
    parameters:
      - name: topic1
        in: query
        type: string
        required: true
        description: The first topic to split
      - name: topic2
        in: query
        type: string
        required: true
        description: The second topic to split
    responses:
      400:
        description: Validation issue. One or both topics were not provided
      500:
		description: Internal server error
      200:
        description: The two topics were splitted
    """
	topic1 = request.args.get('topic1')
	topic2 = request.args.get('topic2')
	if topic1 == None or topic2 == None:
		raise InvalidUsage('provide both topic1 and topic2')
	return "spliting " + topic1 + " " + topic2