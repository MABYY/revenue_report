import os
import csv
import sqlite3

import unittest
import reportgenerator as reportgen

# Temporary file where we use SQLite to perform intermediate calculations
MOCK_DB_FILE = 'mock.db'

PRODUCT_MASTER_FILE = 'TEST_ProductMaster.csv'
SALES_FILE = 'TEST_Sales.csv'
TEAM_MAP_FILE = 'TEST_TeamMap.csv'
READ_DATA_TEST = 'ReadDataTest.csv'
OUTPUT_FILE_TEST = 'TEST_ProductReport.csv'
OUTPUT_TR_TEST = 'TEST_TeamReport.csv'


class TestCalc(unittest.TestCase):

    # Test CSV reading and parsing function read_data. The test confirms that it
    # correctly reads the file and parses the data fields separated by comma.
    def test_read_data(self):

        data = reportgen.read_data(READ_DATA_TEST)
        # test that read_data return value is of the right type
        self.assertEqual(type(data), list,
                         'read_data returned unexpected type, expected list')
        # test that the input test fixture file was read in correctly
        self.assertEqual(len(
            data), 3, 'read_data returned wrong number of lines in test fixture, expeted 3')
        # test that the data in the test fixture file was parse correctly via comma separated values
        for idx, elem in enumerate(data):
            line_num = idx + 1
            self.assertEqual(elem[0].strip(), str(line_num),
                             'read_data returned wrong data value in test fixture at line %d, %d' % (line_num, line_num))
            self.assertEqual(elem[1].strip(), str(2*line_num),
                             'read_data returned wrong data value in test fixture at line %d, %d' % (line_num, 2*line_num))

    # This test ensures that create_db produced the right tables. If the expected tables do not exist,
    # then the SELECT COUNT(*) will fail causing the test to fail.
    def test_create_db(self):

        reportgen.create_db(MOCK_DB_FILE)
        conn = sqlite3.connect(MOCK_DB_FILE)
        cursor = conn.cursor()

        cursor.execute(''' SELECT COUNT(*) FROM product_master ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 0, 'SELECT COUNT(*) FROM product_master returned unexpected number of rows, expeted 0')

        cursor.execute(''' SELECT COUNT(*) FROM sales ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 0, 'SELECT COUNT(*) FROM sales returned unexpected number of rows, expeted 0')

        cursor.execute(''' SELECT COUNT(*) FROM team_map ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 0, 'SELECT COUNT(*) FROM team_map returned unexpected number of rows, expeted 0')

        cursor.close()
        conn.close()

    # This test confirms that load_data function has inserted the right content into our database
    def test_load_data(self):

        reportgen.load_data(PRODUCT_MASTER_FILE, SALES_FILE,
                            TEAM_MAP_FILE, MOCK_DB_FILE)
        conn = sqlite3.connect(MOCK_DB_FILE)
        cursor = conn.cursor()

        cursor.execute(''' SELECT COUNT(*) FROM product_master ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 4, 'SELECT COUNT(*) FROM product_master returned unexpected number of rows, expeted 4')

        cursor.execute(''' SELECT COUNT(*) FROM sales ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 5, 'SELECT COUNT(*) FROM sales returned unexpected number of rows, expeted 5')

        cursor.execute(''' SELECT COUNT(*) FROM team_map ''')
        rows = cursor.fetchall()
        self.assertEqual(
            rows[0][0], 5, 'SELECT COUNT(*) FROM team_map returned unexpected number of rows, expeted 5')

        cursor.close()
        conn.close()

    # # This test that prepare_product_report function writes out the data correctly.
    # # The structure of our db is known, so we can use the values in it as a test fixture
    def test_prepare_product_report(self):
        # remove the output test file if it exists to start the new test
        try:
            os.remove(OUTPUT_FILE_TEST)
        except Exception as e:
            # since this is to clean up the test file, no action is necessary if it does not exist
            pass

        reportgen.prepare_product_report(MOCK_DB_FILE, OUTPUT_FILE_TEST)
        data = reportgen.read_data(OUTPUT_FILE_TEST)
        self.assertEqual(len(
            data), 4, 'output test file for product report contains wrong number of lines, expeted 4')
        self.assertEqual(data[2][1].strip(
        ), '687.5', 'output test file for product report contains wrong data expected 687.5')

    def test_prepare_team_report(self):

        try:
            os.remove(OUTPUT_TR_TEST)
        except Exception as e:
            # since this is to clean up the test file, no action is necessary if it does not exist
            pass

        reportgen.prepare_team_report(MOCK_DB_FILE, OUTPUT_TR_TEST)
        csv_data = []

        with open(OUTPUT_TR_TEST, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in csv_reader:
                csv_data.append(row)

        grossRev = [['Team', 'GrossRevenue'], ['Kings Only', '1000'], [
            'White Knights', '625.0'], ['Kings', '500'], ['Fluffy Bunnies', '312.5']]

        self.assertEqual(csv_data, grossRev)
        print('Team report was correctly generated')

        pass


if __name__ == '__main__':
    unittest.main()
