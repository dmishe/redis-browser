from collections import defaultdict
from redis import Redis
from flask import Flask, render_template, request, g


app = Flask(__name__)

@app.before_request
def before_request():
    g.redis = Redis()
    
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'redis'):
        g.redis.connection_pool.disconnect()

@app.context_processor
def keys():
    keys = defaultdict(list)
    for key in g.redis.keys():
        keys[g.redis.type(key)].append(key)

    return dict(keys=keys)

@app.route('/')
def index():    
    data = None
    key = request.args.get('k')
    if key:
        key_type = g.redis.type(key)
        data = {
            'hash':   lambda x: g.redis.hgetall(x),
            'list':   lambda x: g.redis.lrange(x, 0, -1),
            'string': lambda x: g.redis.get(x),
            'zset':   lambda x: g.redis.zrange(x, 0, -1),
            'set':    lambda x: g.redis.smembers(x)
            
        }[key_type](key)
        
            
    return render_template('index.html', 
        data=data,
        _key=key)

if __name__ == '__main__':
    app.run(debug=True)