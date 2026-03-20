from flask import Flask, jsonify, request

app = Flask(__name__)

PAYMENT = {"price": "0.01 USDC", "wallet": "0x24b288c98421d7b447c2d6a6442538d01c5fce22"}

def kelly(p, b, f=0.5):
    if p <= 0.5 or b <= 0: return 0
    fs = (p*b - (1-p))/b
    return fs*f*100 if fs>0 else 0

@app.route('/')
def index():
    return jsonify({"msg": "Kelly Formula API", "usage": "/?p=0.55&win=5&loss=3", "payment": PAYMENT})

@app.route('/<path:unused>', methods=['GET', 'POST'])
def catch_all(unused):
    p = request.args.get('p', type=float)
    w = request.args.get('win', type=float)
    l = request.args.get('loss', type=float)
    if not all([p,w,l]): return jsonify({"error": "need p, win, loss"})
    return jsonify({"p":p,"win":w,"loss":l,"kelly": round(kelly(p,w/l),2), "payment": PAYMENT})
