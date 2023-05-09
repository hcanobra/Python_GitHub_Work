"""
This script uses a convination of funcitons developed on native Python.

The main function is to create a KLM file from a spread sheet using multiple colums to group elements.

Ver 0.1
Date: 03/02/2020
Author: Hugo Cano
email: hugo.canobravo@verizonwireless.com
WebSite: 

Objective:
    Uses as an imput an Excel file and extracts information to generate menus, submenus, and txt files filtering by
    particular indexes.

main 
    |
    |
    ------ c_main
    |
    ------ c_create_file
    |
    ------ c_create_menu_ip_pool    

How to Run it:

"""

#$language = "Python"
#$interface = "1.0"

import sys
import os

#/ Local path definition
varPath = os.path.dirname(__file__)
if varPath not in sys.path:
    sys.path.insert(0, varPath)

#/ Import local libraries

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')
import csv

def c_main():
    return "Returing back from class c_main from object o_excel_funtion"

# / Begin
#/ Local variable definition
input_filename = sys.argv[1]
x=0


# this is a program to audit the contents of a TXT file
print("START OF PROGRAM")


#/ Call object named File Validation to falidate if the file exist

print ("File that we will work on...", input_filename)




with open(input_filename, newline='') as csvfile:
    csv_dict_reader = csv.DictReader(csvfile)
    csv_records = csv.reader(csvfile)

    column_names = csv_dict_reader.fieldnames
    
    for row in csv_records:
        x=x+1
    

    # print(column_names)

    for records in column_names:
        print (records)

    """
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        print (row)

    """
#input_filename = o_file_validation.c_file_exist ()

#/ Try to open the file
#o_file_validation.c_open_file (input_filename)



# / End



