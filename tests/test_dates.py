# -*- coding: utf-8 -*-
# Example main.py
import argparse
from p1.redact_fun import *


def test_date():

    i_file = '/home/gnani/Project_1/tests/test_file.txt'
    i_out = 'testing'

    with open(i_file, "r") as file:                                # File processing with spacy
            #doc = nlp(file.read())
            result = file.read()

    result, app_data = dates(i_file, result, i_out)

    assert type(result)==str and len(result)>0 and type(app_data)==str and (i_out in app_data)