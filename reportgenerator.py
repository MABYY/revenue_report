#
# This is the main processing module that loads the input data into a SQLite database
# and uses SQL to perform the required calculations. Then the results are read from the database
# and written to output files.
#
# See test_reportgenerator.py for unit tests.

import os
import sys
import csv
import sqlite3


def create_db(db_file):
    try:
        os.remove(db_file)
    except:
        pass

    CREATE_PRODUCTS_TABLE = "CREATE TABLE product_master ( ProductId INT , Name VARCHAR, \
                            Price NUM,  LotSize INT )"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(CREATE_PRODUCTS_TABLE)
    conn.commit()
    conn.close()

    CREATE_TEAMMAP_TABLE = "CREATE TABLE team_map ( TeamId INT , Name VARCHAR)"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(CREATE_TEAMMAP_TABLE)
    conn.commit()
    conn.close()

    CREATE_SALES_TABLE = "CREATE TABLE sales ( SaleId INT , ProductId INT, \
                            TeamId INT , Quantity INT , Discount NUM)"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(CREATE_SALES_TABLE)
    conn.commit()
    conn.close()

    print('Database created')


def read_data(csvFile):
    csv_data = []
    with open(csvFile, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in csv_reader:
            csv_data.append(row)
    return csv_data


def load_data(product_master_file, sales_file, team_map_file, db_file):
    print('Loading data')

    product_master_data = read_data(product_master_file)
    #print(f"PM_csv has {len(product_master_data)} lines" )

    sales_data = read_data(sales_file)
    #print(f"sales_file has {len(sales_data)} lines" )

    team_map_data = read_data(team_map_file)
    #print(f"team_map_file has {len(team_map_data)} lines" )

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    SQL_PARAM_PM = [tuple(row) for row in product_master_data[1:]]
    SQL_COMM_PM = " INSERT INTO product_master (ProductId,Name,Price,LotSize) VALUES (?,?,?,?) "

    cursor.executemany(SQL_COMM_PM, SQL_PARAM_PM)
    conn.commit()

    SQL_PARAM_S = [tuple(row) for row in sales_data[1:]]
    SQL_COMM_S = " INSERT INTO sales (SaleId, ProductId , TeamId , Quantity , Discount) VALUES (?,?,?,?,?) "

    cursor.executemany(SQL_COMM_S, SQL_PARAM_S)
    conn.commit()

    SQL_PARAM_T = [tuple(row) for row in team_map_data[1:]]
    SQL_MM_T = " INSERT INTO team_map (TeamId,Name) VALUES (?,?) "

    cursor.executemany(SQL_MM_T, SQL_PARAM_T)
    conn.commit()

    cursor.close()

    print('Finished data loading')


def prepare_team_report(db_file, team_report_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''SELECT TM.Name as Team, SUM(PM.Price * S.Quantity* PM.LotSize) AS GrossRevenue
                    FROM sales AS S
                    LEFT JOIN product_master as PM
                    ON S.ProductId = PM.ProductId
                    LEFT JOIN team_map as TM
                    ON S.TeamId = TM.TeamId
                    GROUP BY TM.Name
                    ORDER BY GrossRevenue DESC''')

    rows = cursor.fetchall()

    with open(team_report_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Team', 'GrossRevenue'])
        for row in rows:
            writer.writerow(row)

    conn.commit()
    conn.close()


def prepare_product_report(db_file, product_report_file):

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(''' SELECT Name, SUM (Price * S.Quantity * LotSize) AS GrossRevenue,
                        SUM(S.Quantity * LotSize ) AS TotalUnits,
                        SUM (Price * S.Quantity * LotSize * S.Discount/100) AS DiscountCost
                        from product_master as PM
                        LEFT JOIN SALES AS S
                        WHERE PM.ProductId = S.ProductId
                        GROUP BY Name
                        ORDER BY GrossRevenue DESC''')

    rows = cursor.fetchall()

    with open(product_report_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'GrossRevenue', 'TotalUnits', 'DiscountCost'])
        for row in rows:
            writer.writerow(row)

    conn.commit()
    conn.close()
