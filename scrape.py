# Import libraries
import requests
import urllib
import urllib.request
import sys
import csv
import sys
import os
import json
from application import application
from rule import rule
from country_object import country_object

import globals as g


rules_of_origin_scheme_sid = -1
if len(sys.argv) > 1:
    rules_of_origin_scheme_sid = sys.argv[1]

g.app.get_schemes(rules_of_origin_scheme_sid)

for s in g.app.roo_scheme_list:
    my_country = country_object()
    my_country.country = s.code_to_scrape
    my_country.rules_of_origin_scheme_sid = s.rules_of_origin_scheme_sid
    my_country.rules_of_origin_scheme_description = s.description

    g.app.run_local = False
    parse_files = True

    if parse_files:
        for i in range(1, 99):
            chapter = str(i).zfill(2)
            print("Getting rules for chapter " + chapter + " for country " + my_country.country)
            my_rule = rule()
            my_rule.chapter = chapter
            my_rule.country = my_country.country
            my_rule.rules_of_origin_scheme_sid = my_country.rules_of_origin_scheme_sid
            if g.app.run_local:
                path = os.path.join(os.getcwd(), "output/" + my_country.country + "/original/" + my_country.country + "_" + chapter + "_original.html")
                with open(path, 'r') as myfile:
                    my_rule.rule = myfile.read()
            else:
                url = "https://webgate.ec.europa.eu/roo/public/v1//classic/chapter/" + chapter + "/country/" + my_country.country + "?language=EN"
                with urllib.request.urlopen(url) as resource:
                    data = json.loads(resource.read().decode())
                data_item = data[0]
                my_rule.rule = data_item["rules"]

            my_rule.cleanse()
            my_rule.write()

    my_country.write_JSON()
