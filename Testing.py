import mysql.connector

#  Create global connection
connection = mysql.connector.connect(
    host="192.168.0.115",
    user="chemchef_user",   # This user can fetch & delete
    password="spi12345",
    database="ChemChef"
)

#  Function to fetch data
def fetch_data():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM BatchChemical")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        print(" Fetch Error:", err)
    finally:
        cursor.close()

#  Function to delete data by ID
def delete_all_data():
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM BatchChemical"  # removes all rows
        cursor.execute(delete_query)
        connection.commit()
        print(" All records deleted successfully from BatchChemical!")
    except mysql.connector.Error as err:
        print(" Delete Error:", err)
    finally:
        cursor.close()


#  Close connection only once when program exits
def close_connection():
    if connection.is_connected():
        connection.close()
        print(" Connection closed.")

# Example usage
if __name__ == "__main__":
    fetch_data()
    delete_all_data()
    # fetch_data()
    close_connection()
# import mysql.connector
# from mysql.connector import Error
#
# try:
#     connection = mysql.connector.connect(
#         host='192.168.0.112',
#         port=3306,
#         user='chemchef_user',
#         password='spi12345'
#     )
#     if connection.is_connected():
#         print(" MySQL server is running")
# except Error as e:
#     print(f" Cannot connect: {e}")
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()
