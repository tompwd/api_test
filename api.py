import flask
import sqlite3
from flask import request, jsonify
import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)-4d][%(levelname)-8s] %(message)s",
                              datefmt='%Y-%m-%d:%H:%M:%S')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    logger.debug("Home Route Accessed")
    return "<h1>API to access Policy Information</h1>"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# ●	Total policy count for a given user
@app.route('/api/v1/resources/user/policy/count', methods=['GET'])
def api_user_policy_count():
    """Returns count of policies for a given user

    Arguments:
    user_id -- user_id of the user
    month -- month filter formatted as 'YYYY-mm' (OPTIONAL)
    underwriter -- underwriter filter  (OPTIONAL)

    Returns:
    Count of policies for user_id provided
    """

    logger.debug("API Path Accessed: /api/v1/resources/user/policy/count")

    # check for params
    params = {}
    if 'user_id' in request.args:
        params['user_id'] = request.args['user_id']
    else:
        return page_not_found(404)
    if 'month' in request.args:
        params['month'] = request.args['month']
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += 'WHERE '
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"strftime('%Y-%m', policy_start_date) = {str(params[param])}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"select COUNT(*) FROM policy {where_clause}"

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()
    # response_dict = {'count': response}
    conn.close()

    return jsonify(response[0][0])


# ●	Total days active for a given user
@app.route('/api/v1/resources/user/days_active/count', methods=['GET'])
def api_user_days_active_count():
    """Returns number of days active for a given user

    Arguments:
    user_id -- user_id of the user
    month -- month filter formatted as 'YYYY-mm' (OPTIONAL)
    underwriter -- underwriter filter (OPTIONAL)

    Returns:
    Number of days active for a user_id
    """

    logger.debug("API Path Accessed: /api/v1/resources/user/days_active/count")

    # check for params
    params = {}
    if 'user_id' in request.args:
        params['user_id'] = request.args['user_id']
    else:
        return page_not_found(404)
    if 'month' in request.args:
        params['month'] = request.args['month']
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += 'WHERE '
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"strftime('%Y-%m', policy_start_date) = {str(params[param])}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"""with policy_days as
                    (select cast(round(julianday(policy_end_date) - julianday(policy_start_date)) as integer) as days
                        FROM policy {where_clause})
                select SUM(days) from policy_days"""

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()

    conn.close()

    return jsonify(response[0][0])


# ●	Total new user count for a given date
@app.route('/api/v1/resources/policy/new/count', methods=['GET'])
def api_policy_new_count():
    """Returns number of new policies for a given date

    Arguments:
    date -- date to be checked formatted as 'YYYY-mm-dd'
    underwriter -- underwriter filter (OPTIONAL)

    Returns:
    Number of days active for a user_id
    """

    logger.debug("API Path Accessed: /api/v1/resources/policy/new/count")

    # check for params
    params = {}
    if 'date' in request.args:
        params['date'] = request.args['date']
    else:
        return page_not_found(404)
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += 'WHERE policy_start_date = inception AND '
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'date':
            where_clause += f"date(policy_start_date) = {params[param]}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"""with new as (select user_id, min(policy_start_date) inception FROM policy group by user_id)
                , filtered_as_new as (select p.*, n.inception from policy p left join new n on p.user_id =n.user_id)
                select COUNT(*) from filtered_as_new {where_clause}"""

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()

    conn.close()

    return jsonify(response[0][0])


# ●	Total lapsed user count for a given month
@app.route('/api/v1/resources/policy/lapsed/count', methods=['GET'])
def api_policy_lapsed_count():
    """Returns number of lapsed users for a given month

    Arguments:
    month -- month filter formatted as 'YYYY-mm'
    underwriter -- underwriter filter (OPTIONAL)

    Returns:
    Number of lapsed users for a month provided
    """

    logger.debug("API Path Accessed: /api/v1/resources/policy/lapsed/count")

    # check for params
    params = {}
    if 'month' in request.args:
        params['month'] = request.args['month']
    else:
        return page_not_found(404)
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += "WHERE user_lifecycle_status = 'lapsed' AND "
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"year_month = {str(params[param])}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"""with underwriter as (select user_id, underwriter from policy group by user_id, underwriter),
                lifecycle_enriched as (select * from policy_lifecycle pl
                                                left join underwriter u on pl.user_id = u.user_id)
                select COUNT(*) from lifecycle_enriched {where_clause}"""

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()

    conn.close()

    return jsonify(response[0][0])


# ●	Total new users premium per date for a given underwriter
@app.route('/api/v1/resources/policy/new/premium', methods=['GET'])
def api_policy_new_premium():
    """Returns total premium value per day for a given underwriter

    Arguments:
    underwriter -- underwriter filter
    month -- month filter formatted as 'YYYY-mm' (OPTIONAL)

    Returns:
    Total Premium per day
    """

    logger.debug("API Path Accessed: /api/v1/resources/policy/new/premium")

    # check for params
    params = {}
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']
    else:
        return page_not_found(404)
    if 'month' in request.args:
        params['month'] = request.args['month']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += "WHERE policy_start_date = inception AND "
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"strftime('%Y-%m', created_at) = {str(params[param])}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"""with new as (select user_id, min(policy_start_date) inception FROM policy group by user_id)
                , filtered_as_new as (select p.*, n.inception from policy p left join new n on p.user_id =n.user_id)
            select date(created_at) date, SUM(premium) total_new_premium from finance
            left join filtered_as_new
            on finance.policy_id = filtered_as_new.policy_id {where_clause} group by date(created_at)"""

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()

    conn.close()

    return jsonify(response)


# ●	pull all policy data
@app.route('/api/v1/resources/policy', methods=['GET'])
def api_policy():
    """Returns information from the policy table

    Arguments:
    underwriter -- underwriter filter (OPTIONAL)
    month -- month filter formatted as 'YYYY-mm' (OPTIONAL)

    Returns:
    Policy table data with filters specified applied to the table
    """

    logger.debug("API Path Accessed: /api/v1/resources/policy")

    # check for params
    params = {}
    if 'month' in request.args:
        params['month'] = request.args['month']
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

    logger.debug(f"Parameters Passed: {params}")

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += 'WHERE '
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"strftime('%Y-%m', policy_start_date) = {str(params[param])}"
        else:
            where_clause += f'{param} = {params[param]}'

    logger.debug(f"Where Clause Constructed: {where_clause}")

    query = f"""select * from policy {where_clause}"""

    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    response = cur.execute(query).fetchall()

    conn.close()

    return jsonify(response)


if __name__ == '__main__':
    app.run()
