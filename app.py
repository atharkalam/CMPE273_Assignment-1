from flask import Flask, request, jsonify
import rocksdb
import sys
from io import StringIO
import contextlib

app = Flask(__name__)

script_id = 123455

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

@app.route('/api/v1/scripts', methods=['POST'])
def postmethod():
    db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing=True))
    global script_id
    script_id =script_id + 1      
    k=(str(script_id)).encode('utf-8')
    value=(request.files['data'])
    content = value.stream.read()
    u = content.decode('utf-8')
    u=u.encode('utf-8')
    db.put(k,u)
    response=jsonify(script_id=script_id)
    response.status_code=201
    return response 

@app.route('/api/v1/scripts/<string:script_id>', methods=['GET'])
def getmethod(script_id):
    db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing=True))
    key = script_id.encode()
    script_fetch = db.get(key)
    with stdoutIO() as script:
        exec(script_fetch)
    return script.getvalue()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
