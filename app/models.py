from app import db


class Buyer(db.Model):
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # User Info
    etsy_email = db.Column(db.String(50), unique=False, nullable=False)
    updated_email = db.Column(db.String(50), unique=False, nullable=True)
    # Relationships
    transactions = db.relationship('Transaction', backref='buyer', lazy=True)

    def __repr__(self):
        return f'<Buyer {self.id}>'
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'etsy_email': self.etsy_email,
            'updated_email': self.updated_email,
            'transactions': [t.id for t in self.transactions],
            # Extra properties worth returning
            'contact_email': self.updated_email if self.updated_email is not None else self.etsy_email
        }


class Transaction(db.Model):
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Direct Transaction Info
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    sku = db.Column(db.String(20), unique=False, nullable=False)
    receipt_id = db.Column(db.Integer, unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    # Status Booleans
    shipped = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    # Relationships
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    posters = db.relationship('Poster', backref='transaction', lazy=True)

    @property
    def map_type(self):
        # first half of the sku code in lower case
        # skus look like this: MAPTYPE-SIZE
        return self.sku.split('-')[0].lower()
    
    @property
    def is_digital(self):
        # digital posters are defined by a size of D in the sku
        return self.sku.split('-')[-1] == 'D'

    def __repr__(self):
        return f'<Transaction {self.id}>'
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'sku': self.sku,
            'receipt_id': self.receipt_id,
            'quantity': self.quantity,
            'shipped': self.shipped,
            'buyer_id': self.buyer_id,
            'posters': [p.id for p in self.posters]
        }


class Poster(db.Model):
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(50), unique=False, nullable=True)
    # Status Booleans
    responded = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    approved = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    made = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    sent = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    # Relationships
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    response = db.relationship('Response', backref='poster', uselist=False)


    @property
    def map_type(self):
        # first half of the sku code in lower case
        # skus look like this: MAPTYPE-SIZE
        return self.sku.split('-')[0].lower()
    
    @property
    def is_digital(self):
        # digital posters are defined by a size of D in the sku
        return self.sku.split('-')[-1] == 'D'

    def __repr__(self):
        return f'<Poster {self.id}>'
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'responded': self.responded,
            'approved': self.approved,
            'made': self.made,
            'sent': self.sent,
            'transaction_id': self.transaction_id,
            'response_id': self.response.id if self.response is not None else None
        }


class Response(db.Model):
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # All Responses
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    map_datetime = db.Column(db.DateTime, unique=False, nullable=False)
    map_written_datetime = db.Column(db.String(40), unique=False, nullable=True)
    message = db.Column(db.Text, unique=False, nullable=False)
    map_written_address = db.Column(db.Text, unique=False, nullable=False)
    size = db.Column(db.String(20), unique=False, nullable=True) # This could be from the form for a digital poster or from the variations for a phyisical poster
    latitude = db.Column(db.Float, unique=False, nullable=True)
    longitude = db.Column(db.Float, unique=False, nullable=True)
    # Starmap Only
    colour = db.Column(db.String(10), unique=False, nullable=False)
    font = db.Column(db.String(20), unique=False, nullable=False)
    # Watercolour Only
    show_conlines = db.Column(db.Boolean, unique=False, nullable=True)
    map_background = db.Column(db.String(10), unique=False, nullable=True)
    # Relationships
    poster_id = db.Column(db.Integer, db.ForeignKey('poster.id'), nullable=False)

    def __str__(self):
        return f'<Response {self.id}, poster_id={self.poster_id}>'
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'map_datetime': self.map_datetime,
            'map_written_datetime': self.map_written_datetime,
            'message': self.message,
            'map_written_address': self.map_written_address,
            'size': self.size,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'colour': self.colour,
            'font': self.font,
            'show_conlines': self.show_conlines,
            'map_background': self.map_background,
            'poster_id': self.poster_id,
        }