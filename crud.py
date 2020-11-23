"""CRUD operations."""

from model import db, User, Drug, Device, connect_to_db

# Functions start here!
def create_user(email, password, fname, lname, tel_num, caregiver_email):
    """Create and return a new user."""

    user = User(email=email, 
                password=password, 
                fname=fname, 
                lname=lname, 
                tel_num=tel_num, 
                caregiver_email=caregiver_email)

    db.session.add(user)
    db.session.commit()

    return user

def update_user(user_id, fname, lname, email, password, tel_num, caregiver_email):
    """update user information"""
    
    user = User.query.filter(User.user_id == user_id).first()
    user.fname = fname
    user.lname = lname
    user.email = email
    user.password = password
    user.tel_num = tel_num
    user.caregiver_email = caregiver_email

    db.session.commit()

    return user

def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by id"""

    return User.query.filter(User.user_id == user_id).first()
    
def check_user_login_info(email, password):
    """check if the users email and password match in the database"""

    return User.query.filter((User.email == email) & (User.password == password)).first()

def get_password(email):
    """get the pwd for the email and decode it to check login info"""

    return User.query.filter(User.email == email).first()    

def add_device(name, model_num, serial_num, mname, user_id):
    """add a new device for a user."""

    device = Device(device_name=name,
                    model_num=model_num,
                    serial_num=serial_num,
                    manufacturer=mname,
                    user_id=user_id)

    db.session.add(device)
    db.session.commit()

    return device

def update_device(id, device_name, model_num, serial_num, mname, user_id):
    """update device information"""
    
    device = Device.query.filter(Device.id == id).first()
    device.device_name = device_name
    device.model_num = model_num
    device.serial_num = serial_num
    device.manufacturer = mname
    device.user_id = user_id

    db.session.commit()

    return device

def delete_device(id):
    """delete device for the user"""
    Device.query.filter(Device.id == id).delete()
    db.session.commit()

def get_devices_by_user_id(user_id):
    """Return all devices by user id"""

    return Device.query.filter(Device.user_id == user_id).all()

def add_drug(name, mname, user_id):
    """add a new drug for a user."""

    drug = Drug(drug_name=name,
                manufacturer=mname,
                user_id=user_id)

    db.session.add(drug)
    db.session.commit()

    return drug

def update_drug(id, drug_name, mname, user_id):
    """update drug information"""
    
    drug = Drug.query.filter(Drug.id == id).first()
    drug.drug_name = drug_name
    drug.manufacturer = mname
    drug.user_id = user_id

    db.session.commit()

    return drug

def delete_drug(id):
    """delete drug for the user"""
    Drug.query.filter(Drug.id == id).delete()
    db.session.commit()

def get_drugs_by_user_id(user_id):
    """Return all drugs by user id"""

    return Drug.query.filter(Drug.user_id == user_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)