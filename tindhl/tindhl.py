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
            
            if row['Country'] == 'United States of America':
                countryCode = 'USA'
                numberPos   = 'front'

            elif row['Country'] == 'Austria':
                countryCode = 'AUT'
                numberPos   = 'end'

            elif row['Country'] == 'Belgium':
                countryCode = 'BEL'
                numberPos   = 'end'

            elif row['Country'] == 'Bulgaria':
                countryCode = 'BGR'
                numberPos   = 'end'

            elif row['Country'] == 'Croatia':
                countryCode = 'HRV'
                numberPos   = 'end'

            elif row['Country'] == 'Cyprus':
                countryCode = 'CYP'
                numberPos   = 'end'

            elif row['Country'] == 'Czech Republic':
                countryCode = 'CZE'
                numberPos   = 'end'

            elif row['Country'] == 'Denmark':
                countryCode = 'DNK'
                numberPos   = 'end'

            elif row['Country'] == 'Estonia':
                countryCode = 'EST'
                numberPos   = 'end'

            elif row['Country'] == 'Finland':
                countryCode = 'FIN'
                numberPos   = 'end'

            elif row['Country'] == 'France':
                countryCode = 'FRA'
                numberPos   = 'end'

            elif row['Country'] == 'Germany':
                countryCode = 'DEU'
                numberPos   = 'end'

            elif row['Country'] == 'Greece':
                countryCode = 'GRC'
                numberPos   = 'end'

            elif row['Country'] == 'Hungary':
                countryCode = 'HUN'
                numberPos   = 'end'

            elif row['Country'] == 'Ireland':
                countryCode = 'IRL'
                numberPos   = 'end'

            elif row['Country'] == 'Italy':
                countryCode = 'ITA'
                numberPos   = 'end'

            elif row['Country'] == 'Latvia':
                countryCode = 'LVA'
                numberPos   = 'end'

            elif row['Country'] == 'Lithuania':
                countryCode = 'LTU'
                numberPos   = 'end'

            elif row['Country'] == 'Luxembourg':
                countryCode = 'LUX'
                numberPos   = 'end'

            elif row['Country'] == 'Malta':
                countryCode = 'MLT'
                numberPos   = 'end'

            elif row['Country'] == 'Netherlands':
                countryCode = 'NLD'
                numberPos   = 'end'

            elif row['Country'] == 'Poland':
                countryCode = 'POL'
                numberPos   = 'end'

            elif row['Country'] == 'Portugal':
                countryCode = 'PRT'
                numberPos   = 'end'

            elif row['Country'] == 'Romania':
                countryCode = 'ROU'
                numberPos   = 'end'

            elif row['Country'] == 'Slovakia':
                countryCode = 'SVK'
                numberPos   = 'end'

            elif row['Country'] == 'Slovenia':
                countryCode = 'SVN'
                numberPos   = 'end'

            elif row['Country'] == 'Spain':
                countryCode = 'ESP'
                numberPos   = 'end'

            elif row['Country'] == 'Sweden':
                countryCode = 'SWE'
                numberPos   = 'end'

            else:
                countryCode = ''
                numberPos   = 'end'

            # Split street and housenumber if possible
            if numberPos == 'end':
                houseNumber = row['Street'].split(sep= ' ')[-1]
                street      = row['Street'].removesuffix(' ' + houseNumber)
            elif numberPos == 'front':
                houseNumber = row['Street'].split(sep= ' ')[0]
                street      = row['Street'].removeprefix(houseNumber + ' ')
            else:
                houseNumber = row['Street'] 
                street      = row['Street']

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
                'RECV_STREET':      street,
                'RECV_HOUSENUMBER': houseNumber,
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
    with open(output_file, 'w', encoding='UTF-8') as outfile:
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
#################################################a