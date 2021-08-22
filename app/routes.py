from app import app
from app.models import *
from flask import jsonify, request

@app.route('/')
def home():
    return 'Hello World!', 200

# ---------------------------------- BUYER ---------------------------------- #

@app.route('/buyer', methods=['GET'])
def all_buyers():
    if request.method == 'GET':
        bs = Buyer.query.all()
        return jsonify([b.dict for b in bs]), 200

@app.route('/buyer/<buyer_id>', methods=['GET'])
def get_buyer(buyer_id):
    if request.method == 'GET':
        b = Buyer.query.filter_by(id=buyer_id).first()
        return jsonify(b.dict), 200


# ---------------------------------- TRANSACTION ---------------------------------- #

@app.route('/transaction', methods=['GET'])
def all_transactions():
    if request.method == 'GET':
        ts = Transaction.query.all()
        return jsonify([t.dict for t in ts]), 200

@app.route('/transaction/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    if request.method == 'GET':
        t = Transaction.query.filter_by(id=transaction_id).first()
        return jsonify(t.dict), 200


# ---------------------------------- POSTER ---------------------------------- #

@app.route('/poster', methods=['GET'])
def all_posters():
    if request.method == 'GET':
        ps = Poster.query.all()
        return jsonify([p.dict for p in ps]), 200

@app.route('/poster/<poster_id>', methods=['GET'])
def get_poster(poster_id):
    if request.method == 'GET':
        p = Poster.query.filter_by(id=poster_id).first()
        return jsonify(p.dict), 200


# ---------------------------------- RESPONSE ---------------------------------- #

@app.route('/response', methods=['GET'])
def all_responses():
    if request.method == 'GET':
        rs = Response.query.all()
        return jsonify([r.dict for r in rs]), 200

@app.route('/response/<response_id>', methods=['GET'])
def get_response(response_id):
    if request.method == 'GET':
        r = Response.query.filter_by(id=response_id).first()
        return jsonify(r.dict), 200
