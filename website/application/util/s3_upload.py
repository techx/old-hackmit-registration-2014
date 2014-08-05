from base64 import b64encode
from datetime import datetime, timedelta
from json import dumps
import hmac
import sha

from flask import jsonify, current_app, request

from . import bp

def s3_config():
    config = {}
    config['bucket_url'] = current_app.config['AWS_S3_BUCKET_URL']
    config['aws_key_id'] = current_app.config['AWS_ACCESS_KEY_ID']
    return config

policy_routes = {}

def policy_route(**kwargs):
    def make_policy():
        policy_object = {
            'expiration': (datetime.utcnow() + timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'conditions': [
                { 'bucket': 'hackmit-test' },
                { 'acl': 'private' },
                { 'key': policy_context['key'](kwargs) },
                { 'success_action_status': '201' },
                ['content-length-range', '0', '52428800']
            ]
        }
        return b64encode(dumps(policy_object).replace('\n', '').replace('\r', ''))

    def sign_policy(policy):
        return b64encode(hmac.new(current_app.config['AWS_SECRET_ACCESS_KEY'], policy, sha).digest())

    policy_context = policy_routes[str(request.url_rule)]

    if policy_context['permission'] is not None and not policy_context['permission'].can():
        return jsonify({'error': "You do not have permissions for this operation."}), 403

    policy = make_policy()
    return jsonify({
        'policy': policy,
        'signature': sign_policy(policy),
        'key': policy_context['key'](kwargs),
        'success_action_redirect': '/'
    })

def register_policy_route(route, endpoint, permission, key_func):
    bp.add_url_rule(route, endpoint, policy_route)
    policy_routes[route] = {
        'permission': permission,
        'key': key_func
    }
