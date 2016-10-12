# EcommerceParser

HTML parser for ecommerce sites like Amazon and Ebay

Parses product pages with price information and outputs data in the CSV format of:

`URL, Name, Price`

##Usage

`cat html_dump.txt | main.py file_name`

Ecommerce Parser reads lines of html text from stdin and outputs a file `file_name.csv`.


