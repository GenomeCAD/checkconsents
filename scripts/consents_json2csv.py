#!/usr/bin/env python

import argparse
import csv
import json
import os

parser = argparse.ArgumentParser(prog='consents_json2csv.py', description='Convert checkconsents output to csv format')
parser.add_argument('json_filepath')
args = parser.parse_args()

#output_filepath = os.path.join(os.path.dirname(args.json_filepath), os.path.basename(args.json_filepath))
output_filepath = os.path.splitext(args.json_filepath)[0] + '.csv'

#with open('target/CheckConsents_20240918-163024/consents.json', 'r') as f:
with open(args.json_filepath, 'r') as f:
    data = json.load(f)

#with open('target/CheckConsents_20240918-163024/consents.csv', 'w', newline='') as csvfile:
with open(output_filepath, 'w', newline='') as csvfile:
    #writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_STRINGS)
    writer.writerow(['Input directory', 
                     'Input filename', 
                     'Result of the automatic detection', 
                     'Debug image filename', 
                     'Output directory'])
    for d in data:
        img_basename = None
        img_dirname = None
        if d['debug_img_filepath']:
            img_basename = os.path.basename(d['debug_img_filepath'])
            img_dirname = os.path.dirname(d['debug_img_filepath'])
        row = (os.path.dirname(d['pdf_filepath']), 
               os.path.basename(d['pdf_filepath']), 
               d['consent'], 
               img_basename, 
               img_dirname)
        writer.writerow(row)
       # writer.writerow([os.path.dirname(d['pdf_filepath']), os.path.basename(d['pdf_filepath']), d['consent'], os.path.basename(d['debug_img_filepath']), os.path.dirname(d['debug_img_filepath'])])
