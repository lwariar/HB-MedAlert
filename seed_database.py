"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

from crud import *
import model
import server

os.system('dropdb medalert')
os.system('createdb medalert')

model.connect_to_db(server.app)
model.db.create_all()

# add 5 records to the users table
#create_user("testing@test.com", "1111", "Test", "User", "612-222-3333", "testing2@test.com")
#create_user("Phasellus@pharetraNamac.net", "11111", "Timon", "Rivas", "444-109-9485", "lorem.lorem.luctus@sagittisfelisDonec.edu")
#create_user("ullamcorper.eu.euismod@mauriseu.edu", "22222", "Conan", "Patterson", "160-7216", "fringilla.mi.lacinia@dui.net")
#create_user("pede.sagittis.augue@laoreetlibero.ca", "33333", "Hedley", "Hardin", "637-7469", "pharetra.nibh@etmagnis.co.uk")
#create_user("bibendum.Donec.felis@eteuismodet.ca", "44444", "Mikayla", "Brock", "419-958-7077", "lobortis@massa.ca")

# add records to the drugs table
#add_drug("Lohxa", "Lohxa, LLC", 1)
#add_drug("Metformin", "Nostrum Laboratories", 1)

# add records to the devices table
#add_device("TRUE METRIX", "", "", "Trividia Health, Inc.", 1)