
import functools

from flask import *
import json
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/set_watcher', methods=('GET', 'POST'))
def set_watcher():
    if request.method == 'POST':
        from_place = request.form['from_place']
        to_place = request.form['to_place']
        email = request.form['email']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        from_time = request.form['from_time']
        to_time = request.form['to_time']
        error = None

        if not from_place:
            error = 'from_place from missing'
        elif not to_place:
            error = 'to_place to missing'
        if not email:
            error = 'email from missing'
        elif not from_date:
            error = 'from_date to missing'
        if not to_date:
            error = 'to_date from missing'
        elif not from_time:
            error = 'from_time to missing'
        if not to_time:
            error = 'to_time from missing'
        else:
            pass

        if error is None:
            return {"ok":"all ok"}

        json_error = {"error":error}
        return json_error

    return 'anscpa asj'
