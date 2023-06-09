from email import header
import json
import os
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


auth_domain = os.environ.get('AUTH0_DOMAIN')
algorithms = os.environ.get('ALGORITHMS')
api_audience = os.environ.get('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if "Authorization" not in request.headers:
       raise AuthError({
           "code" : "missing_authorization",
           "description" : "Authorization header is expected."
       }, 401)

    auth_header = request.headers["Authorization"]
    header_split = auth_header.split(" ")

    if len(header_split) !=2:
        raise AuthError({
            "code" : "malformed_header",
            "description" : "Authorization header is malformed."
        }, 401)
    elif header_split[0].lower() != "bearer":
        raise AuthError({
            "code" : "invalid_header",
            "description" : "Authorization header does not start with Bearer."
        }, 401)
    
    token = header_split[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            "code" : "invalid_claims",
            "description" : "Permissions not in JWT."
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            "code" : "unauthorized",
            "description" : "Permission not found."
        }, 403)
    
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{auth_domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code' : "invalid_header",
            'description' : "Authorization malformed"
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                "kty" : key["kty"],
                "kid" : key["kid"],
                "use" : key["use"],
                "n" : key["n"],
                "e" : key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = algorithms,
                audience = api_audience,
                issuer = "https://" + auth_domain + "/"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code" : "token_expired",
                "description" : "Token is expired."
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                "code" : "invalid_claims",
                "description" : "Incorrect claims. Please check the audience and issuer."
            }, 401)

        except Exception:
            raise AuthError({
                "code" : "invalid_header",
                "description" : "Unable to parse authentication token."
            }, 400)

    raise AuthError({
        "code" : "invalid_header",
        "description" : "Unable to find the appropriate key."
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort (401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator