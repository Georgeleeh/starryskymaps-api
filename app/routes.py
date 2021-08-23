from app import app
from app.models import *
from flask import jsonify, request
from datetime import datetime
from Etsy import Etsy


@app.route('/')
def home():
    return 'Hello World!', 200


# ---------------------------------- FUNCTIONS ---------------------------------- #

# add the specified transaction to the db, with associated Buyer and Poster
def add_transaction_and_others(etsy_transaction, E=Etsy()):
    # Get buyer_user_id and check if buyer exists in db
    buyer_user_id = etsy_transaction['buyer_user_id']
    b = Buyer.query.filter_by(id=buyer_user_id).first()
    # If not, add the buyer to the db
    if b is None:
        etsy_receipt = E.get_receipt(etsy_transaction['receipt_id'])
        b = Buyer(
            id=buyer_user_id,
            etsy_email=etsy_receipt['buyer_email']
        )

        db.session.add(b)
    
    # Create the Transaction
    t = Transaction(
        id = etsy_transaction['transaction_id'],
        timestamp = datetime.fromtimestamp(etsy_transaction['creation_tsz']),
        sku = etsy_transaction['product_data']['sku'],
        receipt_id = etsy_transaction['receipt_id'],
        quantity = etsy_transaction['quantity'],
        shipped = etsy_transaction['shipped_tsz'] is None,
        buyer_id=b.id
    )

    # Create each Poster required for the Transaction
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
    # Return all Buyers as dicts
    if request.method == 'GET':
        bs = Buyer.query.all()
        return jsonify([b.dict for b in bs]), 200

@app.route('/buyer/<buyer_id>', methods=['GET'])
def get_buyer(buyer_id):
    # Return specified Buyer as dict
    if request.method == 'GET':
        b = Buyer.query.filter_by(id=buyer_id).first()
        return jsonify(b.dict), 200


# ---------------------------------- TRANSACTION ---------------------------------- #

@app.route('/transaction', methods=['GET', 'PUT'])
def all_transactions():
    # Return all transactions as dicts
    if request.method == 'GET':
        ts = Transaction.query.all()
        return jsonify([t.dict for t in ts]), 200

    # Get all open transactions from Etsy and put them in database
    elif request.method == 'PUT':
        added = [] # store added transactions for returning
        E = Etsy()
        etsy_open_transactions = E.get_open_transactions()
        # Add all open transactions, if they don't already exst in db
        for etsy_transaction in etsy_open_transactions.values():
            query = Transaction.query.filter_by(id=etsy_transaction['transaction_id']).first()
            if query is None:
                t = add_transaction_and_others(etsy_transaction, E=E)
                added.append(t)
        # Return ids of added Transactions
        return jsonify([t.id for t in added]), 200

@app.route('/transaction/<transaction_id>', methods=['GET', 'PUT', 'DELETE'])
def transaction(transaction_id):
    # Return specified Transaction as dict
    if request.method == 'GET':
        t = Transaction.query.filter_by(id=transaction_id).first()
        return jsonify(t.dict), 200

    # Put the specified transaction
    elif request.method == 'PUT':
        E = Etsy()
        etsy_transaction = E.get_transaction(transaction_id)
        t = add_transaction_and_others(etsy_transaction, E=E)
        return jsonify(t.dict), 200
    
    # Delete the specified Transaction and associated Posters/Responses
    elif request.method == 'DELETE':
        # Get the Transaction, its Posters/Responses
        t = Transaction.query.filter_by(id=transaction_id).first()
        ps = t.posters
        rs = [p.response for p in ps]

        # Delete Transaction and all found Posters/Responses 
        db.session.delete(t)
        for p in ps:
            db.session.delete(p)
        for r in rs:
            # Responses not guaranteed to exist so check first
            if r is not None:
                db.session.delete(r)

        db.session.commit()
        return {'success' : 'Transaction and orphaned dependents deleted'}, 200


# ---------------------------------- POSTER ---------------------------------- #

@app.route('/poster', methods=['GET'])
def all_posters():
    # Return all Posters as dicts
    if request.method == 'GET':
        ps = Poster.query.all()
        return jsonify([p.dict for p in ps]), 200

@app.route('/poster/<poster_id>', methods=['GET'])
def poster(poster_id):
    # Return specified Poster as dict
    if request.method == 'GET':
        p = Poster.query.filter_by(id=poster_id).first()
        return jsonify(p.dict), 200


# ---------------------------------- RESPONSE ---------------------------------- #

@app.route('/response', methods=['GET'])
def all_responses():
    # Return all Responses as dicts
    if request.method == 'GET':
        rs = Response.query.all()
        return jsonify([r.dict for r in rs]), 200

@app.route('/response/<response_id>', methods=['GET'])
def response(response_id):
    # Return specified Response as dict
    if request.method == 'GET':
        r = Response.query.filter_by(id=response_id).first()
        return jsonify(r.dict), 200
