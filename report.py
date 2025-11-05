#
# This is the auxilary module that reads and parses the arguments from command line
# The main processing code is in the reportgenerator module.
#

import argparse
import reportgenerator as reportgen


# Temporary database file for SQLite processing
DB_REPORT = 'report.db'

parser = argparse.ArgumentParser()


def gen_parse():
    # Read and parse command line arguments
    parser.add_argument("-t", dest="team_map_file", required=True,
                        help="csv-formatted file mapping team id to team name")
    parser.add_argument("-p", dest="product_master_file", required=True,
                        help="csv-formatted file with productId, name, price, and lotsize")
    parser.add_argument("-s", dest="sales_file", required=True,
                        help="csv-formatted file with saleId, productId, teamId, quantity, and discount")
    parser.add_argument("--team-report=", dest="team_report_output_file", required=True,
                        help="gross revenue figures for each team")
    parser.add_argument("--product-report=", dest="product_report_output_file", required=True,
                        help="revenue, units sold, and discount cost for each product")
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = gen_parse()

    # Input files
    team_map_file = args.team_map_file
    product_master_file = args.product_master_file
    sales_file = args.sales_file

    # Output files
    team_report_output_file = args.team_report_output_file
    product_report_output_file = args.product_report_output_file

    # Create database
    reportgen.create_db(DB_REPORT)

    # Populate tables with data in files
    reportgen.load_data(product_master_file, sales_file,
                        team_map_file, DB_REPORT)

    print('Preparing team report')
    reportgen.prepare_team_report(DB_REPORT, team_report_output_file)

    print('Preparing product report')
    reportgen.prepare_product_report(DB_REPORT, product_report_output_file)

    print('Done')
