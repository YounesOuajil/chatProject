import mysql.connector
from mysql.connector import Error 
import json

import os
import sys
# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from model import Resume_Parsing
def connect_insert(data, subject, reference, id_internship):
    try:
        # Connection parameters - adjust as necessary
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mydata'
        )
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            # old method
            # from django.utils import timezone
            # current_datetime = timezone.now()

            # # Insert data into the Intern table
            # insert_query = """INSERT INTO utils_intern (name, email, phone, skills, education, subject, reference, id_internship) 
            #                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            # record = (data['Name'], data['Email'], data['Phone'], ', '.join(data['Skills']), '; '.join(data['Education']), subject, reference, id_internship)
            # cursor.execute(insert_query, record)
            # connection.commit()
            # print("Data inserted successfully into Intern table")
            # ###############
            from utils.models import Intern

            intern = Intern(
                name=data['Name'],
                email=data['Email'],
                phone=data['Phone'],
                skills=data['Skills'],
                education=data['Education'],
                reference=reference,
                subject=subject,
                id_internship=id_internship
            )
            intern.save()
            
            print("Data inserted successfully into Intern table")



    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
# subject = "Internship_2024"
def Resume_Parsing_to_DB(path, subject, reference, id_internship):
    json_data = Resume_Parsing(path)
    data = json.loads(json_data)
    connect_insert(data,subject, reference, id_internship)


# #  usage
# if __name__ == '__main__':
#     folder_path = 'C:/Users/pc/Desktop/Emails Scrapping/Temporary_Attachments'
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.pdf'):  
#             resume_path = os.path.join(folder_path, filename)
#             Resume_Parsing_to_DB(resume_path)
#             os.remove(resume_path)


# with open('resume_data.json', 'w') as json_file:
#         json.dump(json_data, json_file, indent=4)


