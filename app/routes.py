from app import app
from app.models import *
from flask import jsonify, request
from datetime import datetime
from Etsy import Etsy


@app.route('/')
def home():
    return 'Hello World!', 200


# ---------------------------------- FUNCTIONS ---------------------------------- #

def add_transaction_and_others(etsy_transaction, E=Etsy()):
    buyer_user_id = etsy_transaction['buyer_user_id']
    b = Buyer.query.filter_by(id=buyer_user_id).first()
    if b is None:
        etsy_receipt = E.get_receipt(etsy_transaction['receipt_id'])
        b = Buyer(
            id=buyer_user_id,
            etsy_email=etsy_receipt['buyer_email']
        )

        db.session.add(b)

    t = Transaction(
        id = etsy_transaction['transaction_id'],
        timestamp = datetime.fromtimestamp(etsy_transaction['creation_tsz']),
        sku = etsy_transaction['product_data']['sku'],
        receipt_id = etsy_transaction['receipt_id'],
        quantity = etsy_transaction['quantity'],
        shipped = etsy_transaction['shipped_tsz'] is None,
        buyer_id=b.id
    )

    for i in range(t.quantity):
        p = Poster(
            sent=etsy_transaction['shipped_tsz'] is None,
            transaction_id=t.id
        )
        db.session.add(p)
        t.posters.append(p)

    db.session.add(t)
    db.session.commit()
    
    return t


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

@app.route('/transaction/<transaction_id>', methods=['GET', 'PUT', 'DELETE'])
def get_transaction(transaction_id):
    if request.method == 'GET':
        t = Transaction.query.filter_by(id=transaction_id).first()
        return jsonify(t.dict), 200

    elif request.method == 'PUT':
        E = Etsy()
        etsy_transaction = E.get_transaction(transaction_id)
        t = add_transaction_and_others(etsy_transaction, E=E)
        return jsonify(t.dict), 200
    
    elif request.method == 'DELETE':
        t = Transaction.query.filter_by(id=transaction_id).first()
        ps = t.posters
        rs = [p.response for p in ps]

        db.session.delete(t)
        for p in ps:
            db.session.delete(p)
        for r in rs:
            if r is not None:
                db.session.delete(r)

        db.session.commit()
        return {'success' : 'Transaction and orphaned dependents deleted'}, 200


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
