# Revenue Report

Revenue Report is a Python application for calculating aggregated gross revenue and volume figures for teams and products based on sales numbers for a set of unique sales. The Revenue Report module takes as its input three CSV-formatted files and outputs the results into to CSV-formatted files as described in more detail below.

## Prerequisites

The application requires Python 3.x

## Installation

To install the application, uncompress the provided report.zip into the desired directory.

## Usage

You can run the application as follows:

python report.py -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report=TeamReport.csv --product-report=ProductReport.csv

You can perform an internal test of the application by running the following command:

python test_reportgenerator.py

## Input file format

The TeamMap.csv file is a comma-separated text file where each line contains two values: an integer uniquely identifying a team and the string name of the team.

The Product Master file is a comma-separated text file where each line contains information about a unique product. The fields of the file are as follows:

- ProductId – an integer uniquely identifying the Product
- Name – a string name of the Product
- Price – a floating point price at which the Product is sold per unit
- LotSize – an integer representing the number of products sold in a single lot

The Sales file is a comma-separated text file where each line contains information about a unique sale. The fields of the file are as follows:

- SaleId – an integer uniquely identifying the sale
- ProductId – an integer identifying the Product (matches the ProductId from the Product Master)
- TeamId – an integer identifying the Sales Team (matches the TeamId from the Team Map)
- Quantity – an integer representing how many lots of the product were sold
- Discount – a floating point discount percentage given on the sale

## Output file format

The Team Report file is a comma-separated text file where each line contains two values: the string name of the sales team and the total gross revenue of their team’s sales.

The Product Report file is a comma-separated text file where each line summarizes the sales of a single Product and contains four values as follows:

- Name – name of the Product
- GrossRevenue – gross revenue of sales of the Product
- TotalUnits – total number of units sold in the Product
- DiscountCost – total cost of all discounts provided on sales of the Product
# revenue_report
