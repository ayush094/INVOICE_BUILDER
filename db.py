import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",        
        user="ayush",           
        password="ayush@2020", 
        database="invoice2"
    )
