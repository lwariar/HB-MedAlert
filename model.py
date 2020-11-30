""" SQLAlchemy """

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.LargeBinary)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    tel_num = db.Column(db.String(12))
    caregiver_email = db.Column(db.String(50))

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Drug(db.Model):

    __tablename__ = 'drugs'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    drug_name = db.Column(db.String(25))
    manufacturer = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship('User', backref='drugs')

    def __repr__(self):
        return f'<Drug drug_name={self.drug_name} manufacturer={self.manufacturer}>'

class Device(db.Model):

    __tablename__ = 'devices'

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    device_name = db.Column(db.String(25))
    model_num = db.Column(db.String(25))
    serial_num = db.Column(db.String(25))
    manufacturer = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship('User', backref='devices')

    def __repr__(self):
        return f'<Device device_name={self.device_name} manufacturer={self.manufacturer}>'

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Drug.query.delete()
    Device.query.delete()

    # Add user
    user = User("testing@test.com", "1111", "Test", "User", "612-222-3333", "testing2@test.com")

    db.session.add(user)

    # add records to the drugs table
    d1 = Drug("Lohxa", "Lohxa, LLC", 1)
    d2 = Drug("Metformin", "Nostrum Laboratories", 1)

    # add records to the devices table
    d3 = Device("TRUE METRIX", "", "", "Trividia Health, Inc.", 1)

    db.session.add_all([d1, d2, d3])
    db.session.commit()

    leonard = Employee(name='Leonard', dept=dl)
    liz = Employee(name='Liz', dept=dl)
    maggie = Employee(name='Maggie', dept=dm)
    nadine = Employee(name='Nadine')

    db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
    db.session.commit()

def connect_to_db(flask_app, db_uri='postgresql:///medalert', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app

    connect_to_db(app)