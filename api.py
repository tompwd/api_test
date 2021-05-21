import flask
import sqlite3
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>API to access Policy Information</h1>"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# ●	Total policy count for a given user
@app.route('/api/v1/resources/user/policy/count', methods=['GET'])
def api_user_policy_count():

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

    # check for params
    params = {}
    if 'date' in request.args:
        params['date'] = request.args['date']
    else:
        return page_not_found(404)
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

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

    # check for params
    params = {}
    if 'month' in request.args:
        params['month'] = request.args['month']
    else:
        return page_not_found(404)
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']

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

    # check for params
    params = {}
    if 'underwriter' in request.args:
        params['underwriter'] = request.args['underwriter']
    else:
        return page_not_found(404)
    if 'month' in request.args:
        params['month'] = request.args['month']

    # build where clause
    where_clause = ''
    if len(params) > 0:
        where_clause += "WHERE policy_start_date = inception AND "
    for num, param in enumerate(params):
        if num > 0:
            where_clause += ' AND '
        if param == 'month':
            where_clause += f"strftime('%Y-%m', created_at) = {str(params[param]).zfill(2)}"
        else:
            where_clause += f'{param} = {params[param]}'

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


if __name__ == '__main__':
    app.run()
