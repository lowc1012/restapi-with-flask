import os
import pymysql.cursors
import json

from flask import Flask, request, Response

app = Flask(__name__)


def connect_db():
    if app.config["TESTING"] is True:
        conn = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('TEST_MYSQL_USER'),
            password=os.environ.get('TEST_MYSQL_PASSWORD'),
            database=os.environ.get('TEST_MYSQL_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor)
    else:
        conn = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor)
    return conn


@app.route('/tasks', methods=['GET'])
def list_tasks():
    conn = connect_db()

    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM `task`')
            rows = cur.fetchall()
    except pymysql.err:
        return Response('', 500, content_type="application/json")
    finally:
        conn.close()

    return Response(json.dumps({"result": rows}), 200, content_type="application/json")


@app.route('/task', methods=['POST'])
def create_task():
    conn = connect_db()
    try:
        data = request.get_json()
        task_name = data['name']
        if data and "status" in data:
            if data['status'] not in ('1', '0'):
                return Response('', 400, content_type="application/json")
            task_status = data['status']
        else:
            task_status = 0

        with conn.cursor() as cur:
            cur.execute('INSERT INTO `task` (`name`, `status`) VALUES (%s, %s)', (task_name, task_status))
            created_task_id = cur.lastrowid
        conn.commit()

        with conn.cursor() as cur:
            cur.execute('SELECT * FROM `task` WHERE id = %s', created_task_id)
            task = cur.fetchone()
    except (TypeError, KeyError):
        return Response('', 400, content_type="application/json")
    except pymysql.err:
        return Response('', 500, content_type="application/json")
    finally:
        conn.close()

    return Response(json.dumps({'result': task}), 201, content_type="application/json")


@app.route('/task/<int:oid>', methods=['PUT'])
def put_task(oid):
    conn = connect_db()
    status_code = 200
    try:
        data = request.get_json()
        task_id = data['id']
        task_name = data['name']
        task_status = data['status']
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM `task` WHERE id = %s', oid)
            row = cur.fetchone()

        with conn.cursor() as cur:
            if row is None:
                cur.execute('INSERT INTO `task` VALUES (%s, %s, %s)', (task_id, task_name, task_status))
                status_code = 201
            else:
                cur.execute('UPDATE `task` SET id = %s, name = %s, status = %s WHERE id = %s'
                            , (task_id, task_name, task_status, oid))
        conn.commit()

        with conn.cursor() as cur:
            cur.execute('SELECT * FROM `task` WHERE id = %s', task_id)
            task = cur.fetchone()
    except (TypeError, KeyError):
        status_code = 400
        return Response('', status_code, content_type="application/json")
    except pymysql.err:
        status_code = 500
        return Response('', status_code, content_type="application/json")
    finally:
        conn.close()

    return Response(json.dumps(task), status_code, content_type="application/json")


@app.route('/task/<int:oid>', methods=['DELETE'])
def delete_task(oid):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            row = cur.execute('DELETE FROM `task` WHERE id = %s', oid)
        conn.commit()
    except TypeError:
        return Response('', 400, content_type="application/json")
    except pymysql.err:
        return Response('', 500, content_type="application/json")
    finally:
        conn.close()

    if row == 0:
        return Response('', 204, content_type="application/json")

    return Response('', 200, content_type="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
