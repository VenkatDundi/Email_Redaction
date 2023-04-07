# -*- coding: utf-8 -*-
# Example main.py
import argparse
from p1.redact_fun import *
import os


def test_stats():

    i_file = '/home/gnani/Project_1/tests/test_file.txt'
    i_out = 'testing_stats.txt'

    with open(i_file, "r") as file:                                # File processing with spacy
            #doc = nlp(file.read())
            result = file.read()

    result, app_data = ip(i_file, result, i_out)                 # Statistics test with 'dates' redaction
    stats(i_out, app_data)

    assert os.path.exists(i_out) and  len(i_out) > 0                            # Validating if result is being copied to the output path for statistics