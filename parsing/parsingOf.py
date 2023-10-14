import psycopg2
import json
import random
from tqdm import tqdm

conn = psycopg2.connect('postgresql://iremux:pencil@65.109.233.182:5432/branches')

cursor = conn.cursor()

# # Create tables
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS branches (
#     id serial PRIMARY KEY,
#     salePointName VARCHAR(255),
#     address VARCHAR(255),
#     status VARCHAR(255),
#     rko VARCHAR(255),
#     officeType VARCHAR(255),
#     salePointFormat VARCHAR(255),
#     suoAvailability CHAR(1),
#     hasRamp CHAR(1),
#     latitude FLOAT,
#     longitude FLOAT,
#     metroStation VARCHAR(255),
#     distance FLOAT,
#     kep BOOLEAN,
#     myBranch BOOLEAN
# );
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS open_hours (
#     id serial PRIMARY KEY,
#     branch_id int,
#     day VARCHAR(10),
#     hours VARCHAR(50),
#     capacity INT,
#     FOREIGN KEY (branch_id) REFERENCES branches(id)
# )
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS functions (
#     id serial PRIMARY KEY,
#     branch_id int,
#     function_name VARCHAR(255),
#     FOREIGN KEY (branch_id) REFERENCES branches(id)
# )
# """)
#
# cursor.fetchall()

# Load and parse JSON data
with open("offices.txt", "r", encoding='utf-8') as f:
    data = json.load(f)

    # Functions list
    functions_list = [
        "Оформление и обслуживание вкладов",
        "Оформление потребительских и ипотечных кредитов",
        "Выпуск и восстановление карты",
        "Выдача и обмен валюты",
        "Международные переводы",
        "Услуги страхования"
    ]

    # Insert branches data into the database
    for branch in tqdm(data):
        cursor.execute(
            "INSERT INTO branches (salePointName, address, status, rko, officeType, salePointFormat, suoAvailability, hasRamp, latitude, longitude, metroStation, distance, kep, myBranch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (branch['salePointName'], branch['address'], branch['status'], branch['rko'], branch['officeType'],
             branch['salePointFormat'], branch['suoAvailability'], branch['hasRamp'], branch['latitude'],
             branch['longitude'], branch['metroStation'], branch['distance'], branch['kep'], branch['myBranch']))
        branch_id = cursor.fetchone()[0]

        for open_hour in branch['openHours']:
            if open_hour['hours'] == "выходной":
                cursor.execute("INSERT INTO open_hours (branch_id, day, hours, capacity) VALUES (%s, %s, %s, %s)",
                               (branch_id, open_hour['days'], "выходной", 0))
            else:
                try:
                    start_hour, end_hour = map(int, open_hour['hours'].split("-")[0].split(":"))
                    end_hour = int(open_hour['hours'].split("-")[1].split(":")[0]) if "выходной" not in open_hour[
                        'hours'] else start_hour
                    for hour in range(start_hour, end_hour):
                        cursor.execute(
                            "INSERT INTO open_hours (branch_id, day, hours, capacity) VALUES (%s, %s, %s, %s)",
                            (branch_id, open_hour['days'], f"{hour}:00-{hour + 1}:00", random.randint(1, 100)))
                except:
                    pass

        random_functions = random.sample(functions_list, random.randint(2, 6))
        for function in random_functions:
            cursor.execute("INSERT INTO functions (branch_id, function_name) VALUES (%s, %s)", (branch_id, function))

    conn.commit()
    cursor.close()
    conn.close()
