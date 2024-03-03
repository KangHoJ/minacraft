import pandas as pd
import mysql.connector
import time

mariadb_config = #db정보
table_name = 'MoneyTable'
update_interval = 30  

def extract_data():
    try:
        connection = mysql.connector.connect(**mariadb_config)

        if connection.is_connected():
            query = '''
                SELECT m.name , b.level , m.money  
                FROM BankTable b
                INNER JOIN MoneyTable m ON b.name = m.name
            '''
            data = pd.read_sql(query, con=connection)
            # print(data)
            data.to_csv('extracted_data.csv', index=False)
            # csv_df = pd.read_csv('extracted_data.csv')  
            # pantab.frame_to_hyper(csv_df, "minecraft.hyper",table='econumy_join')
            print("추출 및 csv 생성 성공.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Close the database connection
        if connection.is_connected():
            connection.close()
            print("Connection closed.")

def main():
    while True:
        extract_data()
        time.sleep(update_interval)

if __name__ == "__main__":
    main()