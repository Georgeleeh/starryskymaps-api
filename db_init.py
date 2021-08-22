from Etsy import Etsy
from app.models import *
from app import db
from datetime import datetime


db.create_all()

E = Etsy()

etsy_open_transactions = E.get_open_transactions()

for etsy_transaction in etsy_open_transactions.values():
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
