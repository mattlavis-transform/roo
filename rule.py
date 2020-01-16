# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
import re
import os
from lxml import html
from row import row
import globals as g


class rule(object):
    def __init__(self):
        self.country = ""
        self.chapter = ""
        self.rule = ""
        self.rules_of_origin_scheme_sid = ""

    def remove_old_db_records(self):
        sql = "DELETE FROM ml.roo_row WHERE chapter = %s and rules_of_origin_scheme_sid = %s"
        params = [
            self.chapter,
            self.rules_of_origin_scheme_sid
        ]
        cur = g.app.conn.cursor()
        cur.execute(sql, params)
        g.app.conn.commit()

    def cleanse(self):
        self.remove_old_db_records()
        NoneType = type(None)
        self.rule_original = self.rule
        s = self.rule
        if isinstance(s, NoneType):
            self.rule = ""
            return

        s = s.replace("<i>", "")
        s = s.replace("</i>", "")

        s = s.replace("<center>", "")
        s = s.replace("</center>", "")
        s = s.replace(' bgcolor="#FFFFFF"', "")
        s = s.replace(' align="center"', "")
        s = s.replace(' width="100%"', "")
        s = s.replace(' border=0', "")
        # s = s.replace(' width="*"', "")
        s = s.replace(' VALIGN="TOP"', "")
        s = s.replace('<!-- required for colum width -->', "")

        s = self.sr(
            '<th  class="roo"  >Harmonized System classification</th>', "", s)
        s = self.sr(
            '<th class="roo"  colspan=2  >Product specific rule for sufficient production pursuant to Article 5</th>', "", s)

        s = self.sr(' ROWSPAN="*[0-9]"*', "", s)
        s = self.sr(' COLSPAN="*[0-9]"*', "", s)
        s = self.sr(' class="*roo"*', "", s)
        s = self.sr('<div class=chapter></div>', " ", s)
        s = self.sr(' class="*chapter"*', "", s)
        s = self.sr(' valign="*top"*', "", s)
        s = self.sr(' valign="*top"*', "", s)
        s = self.sr(' width="*[0-9]{1,3}%"*', "", s)
        s = self.sr(' width="*[0-9]{1,3}"*', "", s)
        s = self.sr('</a>', "", s)

        # s = self.sr(' class=".+?"', "", s)

        s = s.replace('<TD', "<td")
        s = s.replace('/TD>', "/td>")

        s = s.replace('<TH', "<th")
        s = s.replace('/TH>', "/th>")

        s = s.replace('<CHAPTER>', "")
        s = s.replace('</CHAPTER>', "")

        s = s.replace('<TR', "<tr")
        s = s.replace('/TR>', "/tr>")

        s = self.sr('<td[ ]{1,9}', "<td", s)
        s = self.sr('<th[ ]{1,9}', "<th", s)
        s = s.replace('<td></td>', "")
        s = s.replace('<SUBNOTE>', "<br />")
        s = s.replace('<table >', "")

        s = self.sr('\n{2,5}', "\n", s)
        s = self.sr('<th>\n', "<th>", s)
        s = self.sr('\n</th>', "</th>", s)
        s = self.sr('</td></td>', "</td>", s)
        s = self.sr('<td>\n', "<td>", s)
        s = self.sr('<tr>\n', "<tr>", s)
        s = self.sr('<td></table>', "</table>", s)
        s = self.sr('<tr></table>', "</table>", s)
        s = self.sr('</div>\n', "</div>", s)
        s = self.sr('\n<table>', "<table>", s)

        s = s.replace('<div>', "<br />")
        s = self.sr('<td><br />', "<td>", s)
        s = self.sr(" style='.+?'", "", s)
        s = s.replace('</div>', "")
        s = s.replace('</table></td>', "</td>")
        s = s.replace('<td><td>', "<td>")
        s = s.replace('<br /><tr><td>', "<br />")

        s = s.replace(' align=center', "")
        s = s.replace(' bgcolor=#ffffff', "")

        s = self.sr(' id=".+?"', "", s)
        s = self.sr('<a onclick="openIntroductoryNote\(.+?\)">', "", s)
        s = self.sr('<a onclick="scrollToRoo\(\'.+?\'\)">', "", s)

        s = s.replace('-  ', "- ")
        s = s.replace('&#8211; &#8211; ', "<br />- -")
        s = s.replace('&#8211;', "-")
        s = s.replace('&#8212;', "-")
        s = s.replace('&#8216;', "'")
        s = s.replace('&#8217;', "'")
        s = s.replace('- -', "- - ")
        s = s.replace('&#160;', " ")

        s = self.sr('\[.+?\]', "", s)

        s = self.sr('</span>', "", s)
        s = self.sr('<span>', "", s)
        s = self.sr('\n</tr>', "</tr>", s)
        s = self.sr('<tr></tr>', "", s)
        s = self.sr('Working or processing, carried out on non-originating\n',
                    "Working or processing, carried out on non-originating ", s)

        s = self.sr('<th>HS heading</th>', "", s)
        s = self.sr('<th>Description of product</th>', "", s)
        s = self.sr(
            '<th>Working or processing, carried out on non-originating materials, which confers originating status</th>', "", s)
        for i in range(1, 3):
            s = self.sr('<tr>\n', "<tr>", s)

        s = self.sr('<tr></tr>', "", s)
        s = self.sr('Chapter s', "Chapters", s)
        s = self.sr(r'\n([^<])', r" \1", s)
        s = self.sr(r'ex([0-9]{4})', r"ex \1", s)
        s = s.replace(' %', "%")
        s = s.replace('Manufacture in which:', "Manufacture in which ")
        s = s.replace('Manufacture:', "Manufacture ")
        s = self.sr(
            r'<a class="pointer" onclick="scrollToRoo\(\'.+?\'\)">', "", s)
        s = self.sr('<li> 	', "<br />- ", s)
        s = self.sr('', "", s)

        s = s.replace('<td><br></td>', "")
        s = s.replace('<ul>', "")
        s = s.replace('</ul>', "")
        s = s.replace('\n<br />', "<br />")
        s = s.replace('<tdwidth="*">', "<td>")
        s = s.replace('<tdwidth="*%"', "<td")

        s = s.replace('<br></td>', "</td>")
        s = s.replace('<sup></sup>', "")
        s = s.replace(' class="footnote"', "")
        s = s.replace(' class="Manual_Heading_3"', "")
        s = s.replace('<div class="Normal">', "<br />")
        s = s.replace('<div class="Normal_left">', "<br />")
        s = s.replace('<div class="Normal_Left">', "<br />")
        s = s.replace('<div>', " ")
        s = s.replace('  ', " ")
        s = s.replace('<tr><td>\n</table>', "</table>")
        s = s.replace('\t- -', "<br /> - -")
        s = s.replace(' - -', "<br /> - -")
        s = s.replace('<div class="Normal_Centered">', "")
        s = s.replace('<tdwidth="*" >', "<td>")
        s = s.replace('<td><br />', "<td>")
        s = s.replace('<td> ', "<td>")

        s = s.replace(' CC ', ' CC [Change in Tariff Heading from any other Chapter] ')
        s = s.replace('CTH', 'CTH [Change in Tariff Heading] ')
        s = s.replace('CTSH', 'CTSH [Change in Tariff Subheading] ')
        s = s.replace('RVC', 'RVC [Regional Value Content] ')
        s = s.replace('CTC', 'CTC [Change in Classification] ')
        s = s.replace('SPR', 'SPR [Specific Process Rule] ')
        s = s.replace('EXW', 'EXW [Ex Works] ')
        s = s.replace('FOB', 'FOB [Free on Board] ')
        s = s.replace(
            'MaxNOM', 'MaxNOM [Maximum value of non-originating materials] ')

        s = self.sr('\t', " ", s)
        s = s.replace('  ', ' ')
        s = s.replace('<br /><br />', '<br />')

        self.rule = s

        try:
            tree = html.fromstring(s)
        except:
            return

        html_rows = tree.xpath('//table/tr')
        sequence = 0
        for html_row in html_rows:
            sequence += 1
            html_cells = html_row.xpath('td')
            html_cell_count = len(html_cells)
            cell_texts = []
            record = True

            cell0 = ""
            cell1 = ""
            cell2 = ""
            cell3 = ""

            if self.chapter == "39":
                a = 1

            if html_cell_count > 0:
                try:
                    cell0 = self.get_text(html_cells[0])
                except:
                    pass
            if html_cell_count > 1:
                try:
                    cell1 = self.get_text(html_cells[1])
                except:
                    pass
            if html_cell_count > 2:
                try:
                    cell2 = self.get_text(html_cells[2])
                    a = 1
                except:
                    pass
            if html_cell_count > 3:
                try:
                    cell3 = self.get_text(html_cells[3])
                except:
                    pass

            if self.country in ('JP', 'CA'):
                if html_cell_count == 2:
                    cell_texts.append(cell0)
                    cell_texts.append(cell1)
                    cell_texts.append("")
                else:
                    record = False
            else:
                if html_cell_count == 4:
                    cell_texts.append(cell0)
                    cell_texts.append(cell1)
                    cell_texts.append(
                        (cell2 + "<br />" + cell3))
                elif html_cell_count == 3:
                    if re.match(r'[0-9]{4}', cell0) or re.match(r'ex [0-9]{4}', cell0) or re.match(r'Chapter [0-9]{1,2}', cell0) or re.match(r'ex Chapter [0-9]{1,2}', cell0):
                        cell_texts.append(cell0)
                        cell_texts.append(cell1)
                        cell_texts.append(cell2)
                    else:
                        cell_texts.append("")
                        cell_texts.append(cell0)
                        cell_texts.append(
                            (cell1 + "<br />" + cell2))

                elif html_cell_count == 2:
                    if re.match(r'[0-9]{4}', cell0) or re.match(r'ex [0-9]{4}', cell0) or re.match(r'Chapter [0-9]{1,2}', cell0):
                        cell_texts.append(cell0)
                        cell_texts.append(cell1)
                        cell_texts.append("")
                    else:
                        cell_texts.append("")
                        cell_texts.append(cell0)
                        cell_texts.append(cell1)
                elif html_cell_count == 1:
                    if re.match(r'Chapter [0-9]{1,2}', cell0) or re.match(r'ex [0-9]{4}', cell0):
                        cell_texts.append(cell0)
                        cell_texts.append("")
                        cell_texts.append("")
                    else:
                        cell_texts.append("")
                        cell_texts.append(cell0)
                        cell_texts.append("")
                else:
                    record = False

            # print(html_cell_count)

            if record is True:
                my_row = row()
                my_row.country = self.country
                my_row.chapter = self.chapter
                my_row.rules_of_origin_scheme_sid = self.rules_of_origin_scheme_sid
                my_row.sequence = sequence
                my_row.heading = cell_texts[0]  # .strip()
                my_row.description = cell_texts[1]  # .strip()
                my_row.processing_rule = cell_texts[2]  # .strip()

                my_row.cleanse_specific_columns()
                if my_row.description not in ("(1)"):
                    my_row.persist()

    def sr(self, was, willbe, string):
        source = re.compile(was, re.IGNORECASE | re.DOTALL)
        dest = source.sub(willbe, string)
        return (dest)

    def get_text(self, object):
        s = ""
        items = object.xpath('text()')
        for item in items:
            s += item.strip() + "<br />"

        # s = s.strip("<br />")
        return s

    def write(self):
        path = os.path.join(os.getcwd(), "output")
        folder = os.path.join(path, self.country)
        folder_original = os.path.join(folder, "original")
        folder_filtered = os.path.join(folder, "filtered")
        # print(folder_filtered)

        try:
            os.mkdir(folder)
        except OSError:
            # print("Creation of the directory %s failed" % path)
            pass

        try:
            os.mkdir(folder_filtered)
        except OSError:
            # print("Creation of the directory %s failed" % path)
            pass

        try:
            os.mkdir(folder_original)
        except OSError:
            # print("Creation of the directory %s failed" % path)
            pass

        filename_original = self.country + "_" + self.chapter + "_original.html"
        filename_filtered = self.country + "_" + self.chapter + "_filtered.html"

        file_original = os.path.join(folder_original, filename_original)
        file_filtered = os.path.join(folder_filtered, filename_filtered)

        NoneType = type(None)
        if isinstance(self.rule_original, NoneType):
            self.rule_original = ""

        if g.app.run_local is False:
            f = open(file_original, "w+")
            f.write(self.rule_original)
            f.close()

        f = open(file_filtered, "w+")
        f.write(self.rule)
        f.close()
