import sqlite3


class VragenModel:
    def __init__(self, database_file):
        self.database_file = database_file

    def execute_query(self, sql_query, is_select=True):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result

    def column_query(self, sql_query, is_select=True):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result

    def execute_update(self, sql_query, is_select=True):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql_query)
        conn.commit()

    def get_leerdoel(self):
        query = "SELECT * FROM leerdoelen"
        return self.execute_query(query)

    def get_vragen_without_leerdoel(self):
        query = "SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen) AND uitzondering IS NOT 1 OR leerdoel iS NULL LIMIT 10"
        return self.execute_query(query)

    def save_leerdoel(self, vraag_id, leerdoel_id):
        query = (
            "UPDATE vragen SET leerdoel = " + leerdoel_id + " WHERE id = " + vraag_id
        )
        print(f"Now saving with SQL: {query}")
        self.execute_update(query)

    def exception_leerdoel(self, vraag_id):
        query = "UPDATE vragen SET uitzondering = 1 WHERE id =" + vraag_id
        self.execute_update(query)

    def get_auteur(self):
        query = "SELECT * FROM auteurs"
        return self.execute_query(query)

    def get_vragen_without_auteur(self):
        query = "SELECT * FROM vragen WHERE auteur NOT IN (SELECT id FROM auteurs) OR leerdoel IS NULL LIMIT 10"
        return self.execute_query(query)

    def save_auteur(self, vraag_id, auteur_id):
        query = "UPDATE vragen SET auteur = " + auteur_id + " WHERE id = " + vraag_id
        print(f"Now saving with SQL: {query}")
        self.execute_update(query)

    def get_vragen_with_htmlcodes(self):
        query = "SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;% LIMIT 10'"
        return self.execute_query(query)

    def save_vraag(self, vraag_id, vraag):
        query = f"UPDATE vragen SET vraag = '{ vraag }' WHERE id =  {vraag_id}"
        print(f"Now saving with SQL: {query}")
        self.execute_update(query)

    # def get_vragen_of_selected_auteurs(self, selected_auteurs):
    #     query = "SELECT * FROM vragen WHERE auteur IN (selected_auteurs)"
    #     return self.execute_query(query)

    def get_vragen_of_selected_auteurs(self, selected_auteurs):
        print(selected_auteurs)
        sql_list = str(tuple([key for key in selected_auteurs])).replace(",)", ")")
        query = """
            SELECT * FROM vragen WHERE auteur IN {sql_list}
        """.format(
            sql_list=sql_list
        )
        return self.execute_query(query)

    def get_incorrect_medewerkers(self):
        query = (
            "SELECT * FROM auteurs WHERE medewerker IS NOT 0 AND medewerker IS NOT 1"
        )
        return self.execute_query(query)

    def save_medewerker(self, auteur_id, medewerker_id):
        query = (
            "UPDATE auteurs SET medewerker = "
            + medewerker_id
            + " WHERE  id = "
            + auteur_id
        )
        self.execute_update(query)

    def get_vragen_with_auteur(self):
        query = "SELECT * FROM vragen WHERE auteur BETWEEN 1 AND 17 LIMIT 50"
        return self.execute_query(query)

    def get_uitzondering(self):
        query = "SELECT * FROM vragen WHERE uitzondering IS 1"
        return self.execute_query(query)

    def uitzondering_terugzetten(self, vraag_id):
        query = "UPDATE vragen SET uitzondering = 0 WHERE id IS " + vraag_id
        self.execute_update(query)

    def get_leerdoel_column(self):
        query = "SELECT leerdoel FROM leerdoelen"
        return self.column_query(query)

    def get_auteur_column(self):
        query = "SELECT voornaam, achternaam FROM auteurs"
        return self.column_query(query)
