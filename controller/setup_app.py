from controller.db_service import DBService

class Setup():

    def initial_setup(self):
        
        # Setup Dados Gerais
        db = DBService()
        table_name = "dados_gerais"
        field_list = ["id integer primary key autoincrement", "salario_bruto real", " salario_liquido real"]
        db.create_table(table_name, field_list)

        # Setup despesas_fixas
        table_name = "despesas_fixas"
        field_list = [
            "id integer primary key autoincrement","Descricao text","Categoria text","Valor_Total real","Valor_Mensal real",
            "Status text","Forma_Pagamento text","Qual_Cartao text","Qtd_Meses integer"
        ]
        db.create_table(table_name, field_list)
    
        # Setup despesas_variaveis
        table_name = "despesas_variaveis"
        field_list = [
            "id integer primary key autoincrement","Descricao text","Categoria text","Valor_Total real","Valor_Mensal real",
            "Qual_Cartao text","Parcelas integer","Parcelas_Pagas integer", "Parcelas_Restantes"
        ]
        db.create_table(table_name, field_list)