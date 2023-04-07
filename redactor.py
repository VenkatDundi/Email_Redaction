# -*- coding: utf-8 -*-
# Example main.py
import argparse                                         #
import spacy
import glob
import os
import sys
from p1.redact_fun import *

def main(args):

    if(args.input and len(sys.argv) > 1):                   # Identifies the file format from arguments
        file_format = sys.argv[2]
        
    """ for i in range(len(sys.argv)):
        print(str(i)+'->'+sys.argv[i]) """

    inp = '{}/**/{}'.format(os.path.abspath(os.getcwd()), file_format)      # Constructing a glob expression - "main_folder/**/pattern"

    file_collection = []
    for filename in glob.iglob(inp, recursive=True):                        # glob expression to traverse through sub folders to check the file pattern
        file_collection.append(filename)                                    #print(file_collection)
    
    #nlp = spacy.blank("en")                                     # Blank spacy pipeline with English language
    #nlp = spacy.load('en_core_web_md')                          # Spacy pipeline - (medium) with English language
    #replacement_char = u"\u2588"                                #U+2588 or ALT+219 - Full Block Character
    
    if not os.path.exists(args.output):                         #Validate if the output path already exists
        os.makedirs(args.output)                                    # create directory

    for i_file in file_collection:                      # Traverse through all files in the list
        with open(i_file, "r") as file:                                # File processing with spacy
            #doc = nlp(file.read())
            document = ''.join(file.readlines())
        
        stat_sum = []                                           # List to collect the summary from each function specified in filters
        result = document
        if(args.names):                                         # Check if the filter exists in argument list
            result, app_data = names(i_file, document, args.output)         # redact Names
            stat_sum.append(app_data)                           # Each function call returns - redacted text result and corresponding summary of the function
        
        if(args.genders):                                                   
            result, app_data = genders(i_file, result, args.output)         # redact Genders
            stat_sum.append(app_data)
        
        if(args.dates):
            result, app_data = dates(i_file, result, args.output)           # redact dates
            stat_sum.append(app_data)

        if(args.phones):
            result, app_data = phones(i_file, result, args.output)          # redact phone numbers
            stat_sum.append(app_data)

        if(args.address):
            result, app_data = addresses(i_file, result, args.output)       # redact addresses
            stat_sum.append(app_data)
        
        if(args.ip):
            result, app_data = ip(i_file, result, args.output)       # redact I.P Addresses
            stat_sum.append(app_data)
        
        if(args.stats):                                                        #  Statistics Summary
            args_result = stats(args.stats, stat_sum)
        
        else:                                                                   # Validates to Standard Error if --stats doesn't exist
            sys.stderr.write('Processed file - {}:\n'.format(i_file))
            sys.stderr.write("Summary - {}".format("\n".join(stat_sum)))
    
        file_path = args.output+os.path.basename(i_file)+'.redacted'            # specifying output file pattern

        with open(file_path, 'w') as f:                       # Saving the redacted text to file
            f.write(result)

    
if __name__ == '__main__':                  
    
    parser = argparse.ArgumentParser(description='Redact the given list of Entities in text')   # Argument Parser
    parser.add_argument('--input', type=str, help='Folder with input files', required=True)     # Specifying filters to be detected in arguments
    parser.add_argument('--names', action='store_true', help='redact names')
    parser.add_argument('--dates', action='store_true', help='redact dates')
    parser.add_argument('--phones', action='store_true', help='redact phone numbers')
    parser.add_argument('--genders', action='store_true', help='redact genders')
    parser.add_argument('--address', action='store_true', help='redact addresses')
    parser.add_argument('--ip', action='store_true', help='redact I.P addresses')
    parser.add_argument('--output', type=str, help='output folder', default='.')
    parser.add_argument('--stats', type=str, help='statistics output file', default=None)
    args = parser.parse_args()
    
    if args.input:                  # Validating if --input exists
        main(args)
    else:
        print("Please specify a file pattern using the --input flag.")                  #Error message on missing --input filter




    