import mysql.connector

def insert_batch_chemical():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="192.168.0.200",
            user="erp_user",
            password="erp123",
            database="ChemChef"
        )
        cursor = connection.cursor()

        # Insert query for BatchChemical table
        insert_query = """
            INSERT INTO BatchChemical
            (BatchName, MachineName, FabricWt, MLR, Operator, GroupNo, SeqNo,
             ChemID, TargetWt, TargetTank,DispenseMachine)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Multiple values to insert
        values = [
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 1, 1, 1, 1, "AT1","Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 1, 2, 2, 2, "AT1","Manual"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 1, 3, 3, 3, "AT1","Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 2, 1, 1, 1, "AT1", "Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 2, 2, 2, 2, "AT1", "Manual"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 2, 3, 3, 3, "AT1", "Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 3, 1, 1, 1, "AT1", "Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 3, 2, 2, 2, "AT1", "Manual"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 3, 3, 3, 3, "AT1", "Flow"),
            ("Batch008", "Machine1", 120.5, 1.25, "Operator1", 3, 1, 5, 1, "AT1", "Flow"),
            ("Batch007", "Machine1", 120.5, 1.25, "Operator1", 3, 2, 6, 2, "AT1", "Manual"),
            ("Batch007", "Machine1", 120.5, 1.25, "Operator1", 3, 3, 7, 3, "AT1", "Flow"),
            ("Batch007", "Machine1", 120.5, 1.25, "Operator1", 1, 1, 1, 1, "AT1","Flow"),
            ("Batch007", "Machine1", 120.5, 1.25, "Operator1", 2, 2, 2, 1,"AT1","Manual"),
            ("Batch007", "Machine1", 120.5, 1.25, "Operator1", 3, 3, 3, 2, "AT1","Flow"),
        ]

        cursor.executemany(insert_query, values)
        connection.commit()

        print(f" {cursor.rowcount} rows inserted successfully into BatchChemical by erp_user!")

    except mysql.connector.Error as err:
        print(" Error:", err)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_batch_chemical(batch_name, seq_no):
    """
    Delete a record from BatchChemical based on BatchName and SeqNo.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="192.168.0.200",
            user="erp_user",
            password="erp123",
            database="ChemChef"
        )
        cursor = connection.cursor()

        delete_query = """
            DELETE FROM BatchChemical
            WHERE BatchName = %s AND SeqNo = %s
        """
        cursor.execute(delete_query, (batch_name, seq_no))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"🗑 Record with BatchName={batch_name}, SeqNo={seq_no} deleted successfully!")
        else:
            print(f"⚠ No record found with BatchName={batch_name}, SeqNo={seq_no}")

    except mysql.connector.Error as err:
        print(" Error:", err)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def fetch_data():
    try:
        connection = mysql.connector.connect(
            host="192.168.0.200",
            user="erp_user",
            password="erp123",
            database="ChemChef"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM BatchChemical")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        print(" Fetch Error:", err)
    finally:
        cursor.close()


if __name__ == "__main__":
    delete_batch_chemical("Batch008", 1)
    # insert_batch_chemical()
    fetch_data()
