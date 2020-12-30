import pyodbc


class ConnectToHive():

    def __init__(self):
        self.dsn = "dsn"
        self.user = "user"
        self.password = "password"

    def con_details(self):
        connect_details = "'DSN=" + self.dsn + "; User=" + self.user + ";Password=" + self.password + "', autocommit=True"
        return connect_details


class QueriesHive():

    def __init__(self, tableName):
        self.tableName = "tableToo"

    def run_quiery(self, query):
        con_hive = ConnectToHive()
        # connect to DB Hive
        connection = pyodbc.connect(con_hive.con_details())
        # TODO test the connection details by: print(con_hive.con_details())
        cursor = connection.cursor()
        # parquet command
        cursor.execute("set parquet_fallback_schema_resolution=NAME")
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        connection.commit()
        return results

    def create_table(self, tableName):
        # query to get all table
        query = "CREATE TABLE IF NOT EXISTS " + tableName + "()"
        results = self.run_quiery(query)
        return results

    def get_all_table(self):
        # query to get all table
        query = "SELECT * FROM " + self.tableName
        results = self.run_quiery(query)
        return results

    def add_row(self, dict, tableName):
        # query to add row to table
        values = self.convert_dict_to_values(dict)
        query = "INSERT INTO TABLE " + tableName + " Values(" + values + ");"
        results = self.run_quiery(query)
        return results

    def delete_row(self, oolid):
        # query to delete row in table
        values = "'" + oolid + "'"
        # TODO FIX QUERY
        query = "DELETE TABLE " + self.tableName + " where oolid='" + values + "'"
        results = self.run_quiery(query)
        return results

    def update_row(self, dict):
        # query to update row in table
        # TODO FIX QUERY
        temp_table = "temp"+ dict['date_insertion_partition']
        query_create_temp = "CREATE TABLE "+temp_table + "as (SELECT * FROM " + self.tableName + " where oolid!='" + dict['oolid'] + "' AND date_insertion_partition='" +dict['date_insertion_partition']+"'"
        self.run_quiery(query_create_temp)
        self.add_row(dict, temp_table)
        # TODO test the query_union_table
        query_union_table = "INSERT OVERWRITE "+self.tableName + "date_insertion_partition='"+dict['date_insertion_partition']+"' SELECT * FROM "+temp_table + "DISTRIBUTION BY date_insertion_partition"
        self.drop_table(temp_table)
        # TODO return that update Succeeded
        results = "Succeeded"
        return results

    def get_query_by_value(self, query):
        full_query = "SELECT * FROM " + self.tableName+" WHERE " + query
        results = self.run_quiery(full_query)
        return results

    def drop_table(self, table_name):
        query = "DROP TABLE "+table_name
        self.run_quiery(query)
        # TODO to know if the query run or not

    def convert_dict_to_values(self, dict):
        values = ""
        if 'date_insertion' in dict:
            values = values +"'"+ dict['date_insertion']+ "', "
        else:
            values = values + "'', "
        if 'manId' in dict:
            values = values + "'" + dict['manId'] + "', "
        else:
            values = values + "'', "
        if 'ip' in dict:
            values = values + "'" + dict['ip'] + "', "
        else:
            values = values + "'', "
        if 'birth_date' in dict:
            values = values + "'" + dict['birth_date'] + "', "
        else:
            values = values + "'', "
        if 'last_date' in dict:
            values = values + "'" + dict['last_date'] + "', "
        else:
            values = values + "'', "
        if 'oolId' in dict:
            values = values + "'" + dict['oolId'] + "', "
        else:
            values = values + "'', "
        if 'oolFamily' in dict:
            values = values + "'" + dict['oolFamily'] + "', "
        else:
            values = values + "'', "
        if 'on' in dict:
            values = values + "'" + dict['on'] + "', "
        else:
            values = values + "'', "
        if 'aadName' in dict:
            values = values + "'" + dict['aadName'] + "', "
        else:
            values = values + "'', "
        if 'ik' in dict:
            values = values + "'" + dict['ik'] + "', "
        else:
            values = values + "'', "
        if 'omp' in dict:
            values = values + "'" + dict['omp'] + "', "
        else:
            values = values + "'', "
        if 'unit' in dict:
            values = values + "'" + dict['unit'] + "', "
        else:
            values = values + "'', "
        if 'comments' in dict:
            values = values + "'" + dict['comments'] + "', "
        else:
            values = values + "'', "
        if 'date_insertion_partition' in dict:
            values = values + "'" + dict['date_insertion_partition'] + "', "
        else:
            values = values + "'', "
        return values
