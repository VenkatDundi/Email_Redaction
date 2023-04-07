# -*- coding: utf-8 -*-
# Example main.py
import argparse
import spacy
import glob
from redact_fun import *
import os
import sys

def main(args):

    if(args.input and len(sys.argv) > 1):
        file_format = sys.argv[2]
        
    """ for i in range(len(sys.argv)):
        print(str(i)+'->'+sys.argv[i]) """

    inp = '{}/**/{}'.format(os.path.abspath(os.getcwd()), file_format)

    file_collection = []
    for filename in glob.iglob(inp, recursive=True):
        file_collection.append(filename)                        #print(file_collection)
    
    #nlp = spacy.blank("en")                                    # Blank spacy pipeline with English language
    nlp = spacy.load('en_core_web_sm')                          # Spacy pipeline - (small) with English language

    replacement_char = u"\u2588"                                #U+2588 or ALT+219 - Full Block Character
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    for i_file in file_collection:
        with open(i_file, "r") as file:                                # File processing with spacy
            #doc = nlp(file.read())
            document = file.read()
        
        stat_sum = []
        result = document
        if(args.names):
            result = str(names(i_file, document, args.output)[0])
            stat_sum.append(names(i_file, document, args.output)[1])
        
        if(args.genders):
            result = str(genders(i_file, result, args.output)[0])
            stat_sum.append(genders(i_file, result, args.output)[1])
        
        if(args.dates):
            result = str(dates(i_file, result, args.output)[0])
            stat_sum.append(dates(i_file, result, args.output)[1])

        if(args.phones):
            result = str(phones(i_file, result, args.output)[0])
            stat_sum.append(phones(i_file, result, args.output)[1])

        if(args.address):
            result = str(addresses(i_file, result, args.output)[0])
            stat_sum.append(addresses(i_file, result, args.output)[1])
        
        if(args.stats):
            args_result = stats(args.stats, stat_sum)
        
        else:
            sys.stderr.write('Processed file - {}:\n'.format(i_file))
            sys.stderr.write("Summary - {}".format("\n".join(stat_sum)))
    
        file_path = args.output+os.path.basename(i_file)+'.redacted'

        with open(file_path, 'w') as f:
            f.write(result)

    
if __name__ == '__main__':                  #path = '/home/gnani/Project_1/docs/maildir/bailey-s/all_documents/7.'
    
    parser = argparse.ArgumentParser(description='Redact the given list of Entities in text')
    parser.add_argument('--input', type=str, help='Folder with input files', required=True)
    parser.add_argument('--names', action='store_true', help='redact names')
    parser.add_argument('--dates', action='store_true', help='redact dates')
    parser.add_argument('--phones', action='store_true', help='redact phone numbers')
    parser.add_argument('--genders', action='store_true', help='redact genders')
    parser.add_argument('--address', action='store_true', help='redact addresses')
    parser.add_argument('--output', type=str, help='output folder', default='.')
    parser.add_argument('--stats', type=str, help='statistics output file', default=None)
    args = parser.parse_args()
    
    if args.input:
        main(args)
    else:
        print("Please specify a file pattern using the --input flag.")




    