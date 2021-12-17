from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    # wishlists = db.relationship('Wishlist', backref='user', lazy=True)

    def __repr__(self):
        return f'''
        {self.name},
        {self.number},
        {self.category},
        {self.email},
        {self.username},
        {self.password}
        '''

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pet_type = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(20), nullable=True)
    # user = db.Column('username', db.String(60), db.ForeignKey('user.username'), nullable=True)
    # wishlists = db.relationship('Wishlist', backref='pet', lazy=True)

    def __repr__(self):
        return f'''
        {self.name},
        {self.pet_type},
        {self.age},
        {self.user},
        '''

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    pet_id = db.Column(db.ForeignKey('pet.id'), nullable=False)

    def __repr__(self):
        return f'''
        {self.user_id},
        {self.pet_id},
        '''
