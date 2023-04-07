# -*- coding: utf-8 -*-
# Example main.py
#import argparse
import spacy
import re
import glob

nlp = spacy.load('en_core_web_md')                          # Spacy pipeline - (medium) with English language

replacement_char = u"\u2588"                            # U+2588 or ALT+219 - Full Block Character

def stats(file_name, summary):                          # stats file taking summary as list of strings            

    with open(file_name, 'a') as f:                     # Writing summary to the file - argument passed
        for i in summary:
            f.write(i)
        f.write('\n\n')
    
def ip(file_name, document, out_folder):

    IP = []

    ip_regex = re.compile(
        r'(\b\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\b)')           # I.P Address

    
    ip_format = ip_regex.findall(document)

    for i in ip_format:
        IP.append(i)
        
    for k in IP:
        document = re.sub(r'\b{}\b'.format(re.escape(k)), replacement_char * len(k), document)
        
    l = "File : '{}'\n  Redacted Entities : IP Addresses\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(IP),list(set(IP)),sum(len(s) for s in IP))
    return (document,l)


    
def names(file_name, document, out_folder):

    Names = []                                                  # Names List

    doc = nlp(document)                                         # Processing the text through model - en_core_web_md
    
    for ent in doc.ents:                                        # Entity Capture
        if ent.label_ == "PERSON" or ent.label_ == "ORG":       
            Names.append(ent) 
    ch = Names
    Names = list(set(Names))
    document = str(doc)
    for i in Names: 
        document = re.sub(r'\b{}\b'.format(re.escape(str(i))), replacement_char * len(str(i)), document)        # Substituting the matched words

    Names = list(set([str(i).strip() for i in Names]))      # Unique words found

    # Summary String
    l = "File : '{}'\n  Redacted Entities : NAME\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(Names), list(set(Names)),sum(len(s) for s in ch))
    return (document,l)     #Returing a tuple of redacted text and summary string

def genders(file_name, document, out_folder):

    gen_doc = nlp(document)
    Gend = []
    # Generally used list of pronouns related to genders
    pronouns = ['dad','mr.','male','man','boy','father','son','brother','uncle','grandfather','boyfriend','husband','guy','dude','bachelor','businessman','king','prince','lord','sir','actor','host','waiter','mrs.','ms.','mom','female','woman','mother','Daughter','sister','aunt','grandmother','girlfriend','wife','lady','girl','princess','queen','actress','maid','lady-in-waiting','mother','waitress','hostess']

    for i in gen_doc:                                     
        if i.pos_ == 'PRON':            # Capturing Pronouns
            Gend.append(i)
    
    for i in gen_doc:
        if i.pos_ == 'NOUN' and str(i).lower() in pronouns:         # Validating nouns which exists in the list
            Gend.append(i)

    for j in list(set(Gend)):
        document = re.sub(r'\b{}\b'.format(re.escape(str(j))), replacement_char * len(str(j)), document)

    Gend = list(set([str(i).strip() for i in Gend]))
    l = "File : '{}'\n  Redacted Entities : GENDER\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(Gend),list(set(Gend)),sum(len(s) for s in Gend))
    return (document,l)

def dates(file_name, document, out_folder):

    # Regular Expressions for various date formats
    date_regex = re.compile(
        r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6} (\d{1,2})?[,]?\s?\d{1,4}?(th)?\b|'  # "May 2010" / "September 22" / Dec 5 / July 15th / December 14, 2000
        r'\b(\d{1,2}) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6}[.-]?\s{0,1}\d{1,4}(th)?\b|'  # 13 Dec 2000
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6}[.-]\s{0,1}\d{2}(th)?\b|'   # "Aug. 28th", "July. 12th"
        r'\b\d{1,2}/\d{1,2}\b|'           #"7/11"
        r'\b\d{1,2}-\d{1,2}\b|'             # 25-02
        r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(\w){0,6}, \d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6} \d{2,4}?\b|'     # Saturday, 11 September 2001    /   Monday, April 16, 2001
        r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(\w){0,6}, (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6} \d{1,2}, \d{2,4}?\b|'    # Fri, Mar 18, 2001   /   
        r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(\w){0,6}, (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w){0,6}(.)? \d{1,2}(th)?\b)'     # Wednesday, October 11th   /   Tuesday, Oct. 10th
        )
    
    date_format = date_regex.findall(document)
    Dates = []
    for i in date_format:
        Dates.append(i[0])
        
    for k in Dates:
        document = re.sub(r'\b{}\b'.format(re.escape(k)), replacement_char * len(k), document)
        
    l = "File : '{}'\n  Redacted Entities : DATES\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(Dates),list(set(Dates)),sum(len(s) for s in Dates))
    return (document,l)

def phones(file_name, document, out_folder):

    # Regular Expressions for various phone number formats 
    phone_regex = re.compile(
        r'(\b[+]\d{1,3}(?:.|-|\s)\d{1,3}(?:.|-|\s)\d{1,3}(?:.|-|\s)\d{4}\b|'   #+1 212 641-6663,+44 207 783 2071
        r'\b\d{1,3}(\))?\s?(=)?[\s-]?\d{1,3}[\s-]\d{1,6}\b|'     #(212-310-8000),212-310-8000,212-310-8000.,212 469 5673,12 469-5673, 713-853-1507),=713) 646-3302,713) = 507-6466
        r'\b\d{1,4}\s\d{1,5}\s\d{1,5}?\b|'            # ^\+?\d{1,3}(?=[\s-]?\d{6,14})(-)?\d{1,5}?(-)?\d{1,5}?
        r'\b\d{1,3}[\s-]\d{1,5}[\s-]\d{1,4}\b|'         # 91-11455-25683
        r'\b\d{1}-\d{4}\b)'                             # 3-5083
        )
    
    phone_format = phone_regex.findall(document)

    Phone = []
    
    for i in phone_format:
        Phone.append(i[0])
    
    for k1 in list(set(Phone)):
        document = re.sub(r'\b{}\b'.format(re.escape(k1)), replacement_char * len(k1), document)

    l = "File : '{}'\n  Redacted Entities : PHONE\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(Phone),list(set(Phone)),sum(len(s) for s in Phone))
    return (document,l)

def addresses(file_name, document, out_folder):

    addr = nlp(document)

    Addr = []
    # Generallt used address entities
    lanes = ['north','south','east','west','circle','lane','floor','street','ave','blvd','avenue','st.','rd.','road','av.','ave.','suite']
    
    for i in addr:
        if str(i).lower() in lanes:
            Addr.append(i)

    for ent in addr.ents:
        if ent.label_ == "ADDRESS" or ent.label_ == "GPE":      # Capturing Spacy address entities
            Addr.append(ent.text)
            
    for a in Addr:
        document = re.sub(r'\b{}\b'.format(re.escape(str(a))), replacement_char * len(str(a)), document)

    l = "File : '{}'\n  Redacted Entities : ADDRESS\n  Destination : '{}'\n  Words Redacted = {}\n Unique Words = {}\n  Characters Redacted = {}\n\n".format(file_name,out_folder,len(Addr),list(set(Addr)),sum(len(s) for s in Addr))
    return (document,l)