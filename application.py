import psycopg2
from rules_of_origin_scheme import rules_of_origin_scheme


class application(object):
    def __init__(self):
        self.run_local = False
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            "dbname=tariff_eu user=postgres password=zanzibar")

    def get_schemes(self, rules_of_origin_scheme_sid):
        sql = """
        select roosm.rules_of_origin_scheme_sid, roos.description, roos.abbreviation,
        string_agg(mga.geographical_area_id || ' (' || mga.description || ')', ', ') as countries
        from ml.rules_of_origin_scheme_memberships roosm, ml.rules_of_origin_schemes roos,
        ml.ml_geographical_areas mga
        where roos.rules_of_origin_scheme_sid = roosm.rules_of_origin_scheme_sid
        and roosm.geographical_area_sid = mga.geographical_area_sid
        and roosm.geographical_area_id != 'EH'
        """

        if rules_of_origin_scheme_sid != -1:
            sql += " and roos.rules_of_origin_scheme_sid = " + rules_of_origin_scheme_sid

        sql += "group by 1, 2, 3 order by 1, 2, 3, 4;"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.roo_scheme_list = []
        for row in rows:
            scheme_object = rules_of_origin_scheme(row[0], row[1], row[2], row[3])
            self.roo_scheme_list.append(scheme_object)
