import sys
import re
import globals as g


class row(object):
    def __init__(self):
        self.heading = ""
        self.description = ""
        self.processing_rule = ""
        self.chapter = ""
        self.country = ""
        self.sequence = None
        self.rules_of_origin_scheme_sid = None

    def persist(self):
        sql = """
        INSERT INTO ml.roo_row (heading, description, processing_rule, chapter, country, sequence, rules_of_origin_scheme_sid)
        VALUES  (%s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            self.heading,
            self.description,
            self.processing_rule,
            self.chapter,
            self.country,
            self.sequence,
            self.rules_of_origin_scheme_sid
        ]
        cur = g.app.conn.cursor()
        cur.execute(sql, params)
        g.app.conn.commit()

    def cleanse(self, s):
        s = s.replace("\n", " ")
        s = s.replace("  ", " ")
        s = s.strip()
        s = self.strip_br(s)
        return (s)

    def cleanse_specific_columns(self):
        self.description = self.cleanse(self.description)
        self.processing_rule = self.cleanse(self.processing_rule)

        self.heading = self.sr(r'(ex [0-9]{6}) ', r"\1<br />", self.heading)
        self.heading = self.sr(r'([0-9]{6};) ', r"\1<br />", self.heading)
        self.heading = self.sr(r'([0-9]{4},) ', r"\1<br />", self.heading)

        self.description = self.description.replace('<br />or<br />', '<br /><em>or</em><br />')
        self.processing_rule = self.processing_rule.replace(' and<br />', ' <em>and</em><br />')
        self.processing_rule = self.processing_rule.replace('<br />or<br />', '<br /><em>or</em><br />')
        self.processing_rule = self.processing_rule.replace(' or<br />', ' <em>or</em><br />')
        self.processing_rule = self.processing_rule.replace('<br />Or<br />', '<br /><em>or</em><br />')
        self.processing_rule = self.processing_rule.replace(' Or<br />', ' <em>or</em><br />')

        self.heading = self.heading.replace('<br /><br />', '<br />')
        self.description = self.description.replace('<br /><br />', '<br />')
        self.processing_rule = self.processing_rule.replace('<br /><br />', '<br />')

        self.heading = self.strip_br(self.heading)
        self.description = self.strip_br(self.description)
        self.processing_rule = self.strip_br(self.processing_rule)

        if "Manufacture in which" in self.description or "Manufacture from animals" in self.description:
            if self.heading == "":
                if self.processing_rule == "":
                    self.heading = "Chapter " + self.chapter
                    self.processing_rule = self.description
                    self.description = "&nbsp;"

    def strip_br(self, s):
        if s[-6:] == "<br />":
            s = s[:-6]
        return s

    def sr(self, was, willbe, string):
        source = re.compile(was, re.IGNORECASE | re.DOTALL)
        dest = source.sub(willbe, string)
        return (dest)
