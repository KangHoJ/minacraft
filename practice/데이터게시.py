from tableau_api_lib import TableauServerConnection, ServerConnection
import os

# Tableau Public connection details
tableau_config = # 테블로 계정 정보

# Workbook and data source details
workbook_name = 'test.twb'
csv_file_path = 'extracted_data.csv'
hyper_file_path = 'extracted_data.hyper'

def csv_to_hyper(csv_file_path, hyper_file_path):
    # Convert CSV to Tableau Hyper using tableauhyperapi
    os.system(f'tableau-hyper-api convert -i {csv_file_path} -o {hyper_file_path}')

def publish_to_tableau_public():
    # Connect to Tableau Public using TableauRestApiConnection
    connection = TableauRestApiConnection(server=tableau_config['server'],
                                          username=tableau_config['username'],
                                          password=tableau_config['password'],
                                          version='3.10')  # Choose the appropriate version
    connection.sign_in()

    try:
        # Check if the workbook already exists
        try:
            connection.query_workbooks(name=workbook_name)
            print(f"Workbook '{workbook_name}' already exists on Tableau Public.")
        except ServerResponseError:
            # Convert CSV to Tableau Hyper
            csv_to_hyper(csv_file_path, hyper_file_path)

            # Publish the workbook
            connection.publish_workbook(workbook_name, hyper_file_path)

            print(f"Workbook '{workbook_name}' published to Tableau Public.")

    finally:
        # Sign out from Tableau Public
        connection.sign_out()

def main():
    while True:
        # Extract data from MySQL and create Hyper file
        extract_data()

        # Sleep for the specified interval
        time.sleep(update_interval)

if __name__ == "__main__":
    main()