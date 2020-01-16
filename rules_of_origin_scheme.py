import sys


class rules_of_origin_scheme(object):
    def __init__(self, rules_of_origin_scheme_sid, description, abbreviation, country_string):
        self.rules_of_origin_scheme_sid = rules_of_origin_scheme_sid
        self.description = description
        self.abbreviation = abbreviation
        self.country_string = country_string
        self.code_to_scrape = ""

        self.get_code_to_scrape()

    def get_code_to_scrape(self):
        s = self.country_string
        p = s.find(' (')
        if (p != -1):
            s = s[0:p].strip()
            self.code_to_scrape = s
