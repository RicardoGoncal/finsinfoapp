import sqlite3


class DBService():

    def create_table(self, table_name, fields_list):
        
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()

        fields = ','.join(fields_list)
        # print(fields)

        query = f"""
            create table if not exists {table_name} (
                {fields}
            )
        """
        cursor.execute(query)
        connect_database.commit()
        connect_database.close()


    def get_geral_data(self, table_name):
        
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()

        query = f"select * from {table_name}"
        cursor.execute(query)
        field_keys = ("id", "salario_bruto", "salario_liquido")
        data = []
        rows = cursor.fetchall()

        for row in rows:
            data_dict = dict(zip(field_keys, row))
            data.append(data_dict)

        return data


    def get_df_data(self, table_name):
        
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()

        query = f"select * from {table_name}"
        cursor.execute(query)
        field_keys = ("id", "descricao", "categoria", "valor_total", "valor_mensal", "status", "forma_pagamento", "qual_cartao", "qtd_meses")
        data = []
        rows = cursor.fetchall()

        for row in rows:
            data_dict = dict(zip(field_keys, row))
            data.append(data_dict)

        connect_database.commit()
        connect_database.close()
        return data
    

    def set_df_new_data(self, table_name, values):
        
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()

        query = f"""insert into {table_name} (Descricao, Categoria, Valor_Total, Valor_Mensal, Status, Forma_Pagamento, Qual_Cartao, Qtd_meses) 
                values (?,?,?,?,?,?,?,?)"""
        cursor.execute(query,((values)))

        connect_database.commit()
        connect_database.close()

    
    def update_df_data(self, values, row_id):

        table_name = "despesas_fixas"
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()
        id = row_id

        query = f"""
            update {table_name}
            set Descricao=?, Categoria=?, Valor_Total=?, Valor_Mensal=?, Status=?, Forma_Pagamento=?, Qual_Cartao=?, Qtd_meses=?
            where id = {id}
        """
        cursor.execute(query,((values)))

        connect_database.commit()
        connect_database.close()

    def delete_df_data(self, row_id):

        table_name = "despesas_fixas"
        connect_database = sqlite3.connect('app.db')
        cursor = connect_database.cursor()
        id = row_id

        query = f"delete from {table_name} where id=?"

        cursor.execute(query, (str(id)))

        connect_database.commit()
        connect_database.close()



