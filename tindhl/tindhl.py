#############################################################################
##                              DHLabel                                    ##
#############################################################################
# Command line tool to consolidate several DHL labels 
# for printing with less waste

import os
import sys
import argparse
import configparser
import csv
from appdirs import user_config_dir


#############################################################################
##                           Global variables                              ##
#############################################################################
input_file          = ""
output_path         = ""

#############################################################################
##                               Helpers                                   ##
#############################################################################

def argset():
    """
    Sets command line arguments
    """
    global input_file
    global output_path

    parser = argparse.ArgumentParser(description=
        "Command line tool to consolidate several DHL labels for printing with less waste")

    # Input path
    defaultInputFile = os.getcwd() + "/orders.csv"
    parser.add_argument('input_file', nargs='?', 
        default= defaultInputFile,
        help="""
            Path to input CSV. Uses "orders.csv" in current path by default
            """)

    # Output path
    parser.add_argument('output_path', nargs='?', 
        default=os.getcwd(),
        help="""
            Path of output CSV. Will use 
            current directory if ommited
            """)

    # Parse args
    args = parser.parse_args()
    input_file  = args.input_file
    output_path = args.output_path

    # Output recognized args
    print("Using input path:")
    print(input_file)
    print("Using output path:")
    print(output_path)
    print("---")

    # Argument sanity checks
    if not os.path.isfile(input_file):
        print("The input file specified does not exist, exiting")
        sys.exit()
    if not os.path.isdir(output_path):
        print("The output directory specified does not exist, exiting")
        sys.exit()


def convert(config):
    """
    Convert existing Tindie order export to DHL import
    """
    
    global input_file
    global output_path

    # Generate default output header
    dhlExportHeader = [
        '',
        'SEND_NAME1',
        'SEND_NAME2',
        'SEND_STREET',
        'SEND_HOUSENUMBER',
        'SEND_PLZ',
        'SEND_CITY',
        'SEND_COUNTRY',
        'RECV_NAME1',
        'RECV_NAME2',
        'RECV_STREET',
        'RECV_HOUSENUMBER',
        'RECV_PLZ',
        'RECV_CITY',
        'RECV_COUNTRY',
        'PRODUCT',
        'COUPON',
        'SEND_EMAIL'
    ]

    # Generate empty list
    dhlExportData = []

    # Read in Tindie data
    with open(input_file, newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',', quotechar='"')
         
        tindieExport = [row for row in reader]

    # Iterate through all rows, but only care about unique ones
    for row in tindieExport:
        if row['First Name']:

            print('Dumping Row for ' + row['First Name'] + ' ' + row['Last Name'])

            # Find country code (No idea what other values DHL accepts)
            countryCode = ''
            if row['Country'] == 'Germany':
                countryCode = 'DEU'
                # House number at the end
                
            elif row['Country'] == 'United States of America':
                countryCode = 'USA'
                # House number in front

            # Fill one row of data
            dhlExportSingleRow = {
                '': '',
                'SEND_NAME1':       config['sender']['name'],
                'SEND_NAME2':       config['sender']['name2'],
                'SEND_STREET':      config['sender']['street'],
                'SEND_HOUSENUMBER': config['sender']['house number'],
                'SEND_PLZ':         config['sender']['zipcode'],
                'SEND_CITY':        config['sender']['city'],
                'SEND_COUNTRY':     config['sender']['country'],
                'RECV_NAME1':       row['First Name'] + ' ' + row['Last Name'],
                'RECV_NAME2':       row['Company'],
                'RECV_STREET':      row['Street'],
                'RECV_HOUSENUMBER': row['Street'],
                'RECV_PLZ':         row['Postal/Zip Code'],
                'RECV_CITY':        row['City'],
                'RECV_COUNTRY':     countryCode,
                'PRODUCT':          '',
                'COUPON':           '',
                'SEND_EMAIL':       config['sender']['email']
            }

            # Add data to new shipping row
            dhlExportData.append(dhlExportSingleRow)

    # Create new output file
    output_file = os.path.join(output_path, "TinDHL.csv")
    with open(output_file, 'w') as outfile:
        writer = csv.DictWriter(outfile, dhlExportHeader, delimiter=',')
        
        writer.writeheader()
        writer.writerows(dhlExportData)


    print("---")
    print("Conversion done")
    print("---")

#############################################################################
##                               main()                                    ##
#############################################################################
def main():
    print("--------------------")
    print("--Starting  TinDHL--")
    print("--------------------")

    # User config handling
    config_dir          = user_config_dir("TinDHL")
    user_config_path    = os.path.join(config_dir, "config.toml")
    config              = configparser.ConfigParser()

    # Create path to user config
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # Create config file if it doesn't exist
    if not os.path.isfile(user_config_path):
        print("""
            Default config file did not exist. 
            Please manually enter your default values in the following file:
            """)
        print(user_config_path)

        config['sender'] = {'name':             'Danny Default',
                            'name2':            'Dannies Co.',
                            'street':           'Rad Rd',
                            'house number':     '666',
                            'zipcode':          '12345',
                            'city':             'Tubular Town',
                            'country':          'USA',
                            'email':            'DannyDefault@Radmail.com',}

        with open(user_config_path, 'w') as configfile:
            config.write(configfile)

        sys.exit()

    # Read existing user config 
    with open(user_config_path, 'r') as configfile:
        config.read(user_config_path)

    # Set command line arguments
    argset()

    # Create spliced file
    convert(config)


#############################################################################
##                         main() idiom                                    ##
#############################################################################
if __name__ == "__main__":
    main()