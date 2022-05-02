from app import db 


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    mid_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    
    
    def __repr__(self):
        return "<Users %r>" %self.username