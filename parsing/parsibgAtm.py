import psycopg2
import json
from tqdm import tqdm

conn = psycopg2.connect('postgresql://iremux:pencil@65.109.233.182:5432/branches')

cursor = conn.cursor()


# CREATE TABLE services (
# 	id serial PRIMARY KEY,
# 	name varchar NOT NULL
# );
#
# INSERT INTO services (name) VALUES ('wheelchair');
# INSERT INTO services (name) VALUES ('blind');
# INSERT INTO services (name) VALUES ('nfcForBankCards');
# INSERT INTO services (name) VALUES ('qrRead');
# INSERT INTO services (name) VALUES ('supportsUsd');
# INSERT INTO services (name) VALUES ('supportsChargeRub');
# INSERT INTO services (name) VALUES ('supportsEur');
# INSERT INTO services (name) VALUES ('supportsRub');

# CREATE TABLE services_of_atm (
# 	id serial PRIMARY KEY,
# 	serviceCapability varchar(50),
# 	serviceActivity varchar(50),
# 	service_id int not null,
# 	atm_id int not null,
# 	FOREIGN KEY (atm_id) REFERENCES atms(id),
# 	FOREIGN KEY (service_id) REFERENCES services(id)
# );

# CREATE TABLE atms (
# 	id serial PRIMARY KEY,
#     address varchar(255),
# 	latitude float8,
# 	longitude float8,
# 	allDay bool
# );


services = {
        "wheelchair": 1,
        "blind": 2,
        "nfcForBankCards": 3,
        "qrRead": 4,
        "supportsUsd": 5,
        "supportsChargeRub": 6,
        "supportsEur": 7,
        "supportsRub": 8,
    }

with open("atms.txt", "r", encoding='utf-8') as f:
    data = json.load(f)


    # Insert branches data into the database
    for branch in tqdm(data['atms']):
        cursor.execute(f"INSERT INTO atms (address, latitude, longitude, allday) VALUES ('{branch['address']}', {branch['latitude']}, {branch['longitude']}, {branch['allDay']}) RETURNING id")
        atm_id = cursor.fetchone()[0]

        for service in branch['services']:
            cursor.execute(f"INSERT INTO services_of_atm (serviceCapability, serviceActivity, service_id, atm_id) VALUES ('{branch['services'][service]['serviceCapability']}', '{branch['services'][service]['serviceActivity']}', {services[service]}, {atm_id})")


    conn.commit()
    cursor.close()
    conn.close()
