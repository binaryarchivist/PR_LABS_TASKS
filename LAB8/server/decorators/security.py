from flask import request

from functools import wraps
from datetime import datetime

from ..database.database import db
from ..models.token import Token


def secured(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        access_token = request.headers.get('X-Access-Token')
        if access_token is None:
            return {"message": "Please provide an Access Key to access this resource"}, 400
        elif is_valid(access_token):
            token = Token.query.filter_by(token=access_token).first()
            token.used = True
            db.session.commit()

            Token.query.filter(Token.expiration_time < datetime.now()).delete()
            db.session.commit()  # deleting token after use
            return func(*args, **kwargs)
        else:
            return {"message": "The provided Access Key is not valid"}, 403

    return decorator


def is_valid(token_str: str) -> bool:
    token = Token.query.filter_by(token=token_str).first()
    if token and not token.used and token.expiration_time > datetime.now():
        return True
    return False
