import customtkinter as ctk
from PIL import Image
from tkinter import *
from tkinter import ttk
from controller.db_service import DBService
from controller.calc_service import CalcService
from controller.setup_app import Setup
from configparser import ConfigParser
from tkinter import messagebox



# Cria a janela do aplicativo
window = ctk.CTk()

# Instanciar setup
setup = Setup()

# Instanciar db_service e calc_service
db = DBService()
calc = CalcService()


# Iniciar ConfigParser
config = ConfigParser()

# Classe principal do aplicativo
class MainApp():
    def __init__(self):
        self.window = window
        self.db = db
        self.calc = calc
        self.config = config
        self.theme()
        self.frame_initial_config()
        self.welcome_frame = None
        self.frame_base = None
        self.frame_df = None
        self.initial_frame()
        window.mainloop()


    def setup(self):
        # Criar tabelas no banco de dados
        # config.ini (dados_gerais = 0)
        self.config.read("config.ini")
        cfg_geral_data = self.config.get("setup", "dados_gerais")
        if int(cfg_geral_data) == 0:
            print("configurando....")
            setup.initial_setup()
            self.config.set("setup", "dados_gerais", "1")

            with open('config.ini', 'w') as cfg:
                self.config.write(cfg)
        

    def theme(self):
        ctk.set_appearance_mode("system")


    def frame_initial_config(self):
        # Configuração da Tela
        self.window.geometry("1000x500")
        self.window.title("Finsinfo")
        self.window.resizable(width=True, height=True)

        # Faz o SETUP Inicial
        self.setup()
        

    def initial_frame(self):

        # Design da Tela Inicial
        self.welcome_frame = ctk.CTkFrame(master=self.window, width=1000, height=500, fg_color="white")
        self.welcome_frame.pack()
        label_img = ctk.CTkLabel(master=self.welcome_frame, image=PhotoImage(file="./image/logo2.png"), text="").place(x=225, y=75)
        nome_img = ctk.CTkLabel(master=self.welcome_frame, image=PhotoImage(file="./image/nome_programa.png"), text="").place(x=250, y=5)
        entrar_button = ctk.CTkButton(master=self.welcome_frame, text="Entrar", fg_color="#FEB403", command=self.base_frame).place(x=320, y=430)
       
        

    def base_frame(self):

        # Monta o frame novo
        self.welcome_frame.pack_forget()
        self.frame_base = ctk.CTkFrame(master=self.window, width=1000, height=500, fg_color="white")
        self.frame_base.pack()

        # Variaveis para preencher Labels
        general_data = self.db.get_geral_data("dados_gerais")
        salario_bruto = general_data[0]["salario_bruto"]
        salario_liquido = general_data[0]["salario_liquido"]

        # Acrescenta Widgets de Botao no frame
        btn_despesas_fixas = ctk.CTkButton(master=self.frame_base, text="Despesas Fixas", fg_color="#FEB403", command=self.tela_despesas_fixas).place(x=10, y=70)
        # btn_despesas_variaveis = ctk.CTkButton(master=self.frame_base, text="Despesas Variaveis", fg_color="#FEB403", command=self.tela_despesas_variaveis).place(x=10, y=120)
        # btn_limite_gastos_categoria = ctk.CTkButton(master=self.frame_base, text="Lim. Categorias", fg_color="#FEB403").place(x=10, y=170)
        # btn_atual_dados_gerais = ctk.CTkButton(master=self.frame_base, text="Atual. Dados Gerais", fg_color="#FEB403", command=self.popup_dados_gerais).place(x=10, y=220)

        # Acrescenta Widgets de Label no frame
        salario_bruto_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Bruto: {salario_bruto}", font=("Robot", 16)).place(x=10, y= 10)
        salario_liquido_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Liquido: {salario_liquido}", font=("Robot", 16)).place(x=180, y= 10)

    

    def tela_despesas_fixas(self):
        # Monta o frame novo
        self.frame_base.pack_forget()
        self.frame_df = ctk.CTkFrame(master=self.window, width=1000, height=500, fg_color="white")
        self.frame_df.pack()

        area_title = ctk.CTkLabel(master=self.frame_df, text=f"Despesas Fixas", font=("Robot", 20)).place(relx=.5, y=15, anchor="center")
        
        def back_frame():
            self.frame_df.pack_forget()
            self.frame_base.pack()

        
        def update_item(event):

            item = table.identify("item", event.x, event.y)
            values = table.item(item)['values']
            self.popup_nova_df(acao="attdel", valores=values)


        # Area dos botoes
        btn_voltar = ctk.CTkButton(master=self.frame_df, text="Voltar", fg_color="#FEB403", command=back_frame).place(relx=.80, rely=.9)
        btn_novo = ctk.CTkButton(master=self.frame_df, text="Novo", fg_color="#FEB403", command=self.popup_nova_df).place(relx=.02, rely=.7)
        # btn_atualizar = ctk.CTkButton(master=self.frame_df, text="Atualizar", fg_color="#FEB403").place(relx=.20, rely=.7)
        # btn_deletar = ctk.CTkButton(master=self.frame_df, text="Deletar", fg_color="#FEB403").place(relx=.38, rely=.7)


        # Criar tabela
        columns = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        categories = ("Id", "Descricao","Categoria","Valor Total","Valor Mensal","Status","Forma Pagam.","Cartao","Qtd_Meses")
        table = self.criar_tabela(self.frame_df, columns, categories)
        table.place(x=20, rely=.15)

        # Inserir dados na tabela
        data_table = self.db.get_df_data("despesas_fixas")
        for row in data_table:
            values = (row["id"], row["descricao"], row["categoria"], row["valor_total"], row["valor_mensal"],
                      row["status"], row["forma_pagamento"], row["qual_cartao"], row["qtd_meses"])
            table.insert(parent='', index="end", values=values)

        # Deixa o item da tabela com Double Click para abrir as opcoes de deletar ou atualizar
        table.bind("<Double-1>", update_item)
        

        
    # def tela_despesas_variaveis(self):
    #     # Monta o frame novo
    #     self.frame_base.pack_forget()
    #     self.frame_dv = ctk.CTkFrame(master=self.window, width=800, height=500, fg_color="white")
    #     self.frame_dv.pack()

    #     titulo_area = ctk.CTkLabel(master=self.frame_dv, text=f"Despesas Variaveis", font=("Robot", 20)).place(relx=.5, y=15, anchor="center")

    #     def voltar_tela():
    #         self.frame_dv.pack_forget()
    #         self.frame_base.pack()

    #     btn_voltar = ctk.CTkButton(master=self.frame_dv, text="Voltar", fg_color="#FEB403", command=voltar_tela).place(relx=.01, rely=.9)


    # def popup_dados_gerais(self):

    #     def salvar_dados_gerais():
    #         # Coleta as infos do EntryCTk
    #         sb = input_salario_bruto.get()
    #         sl = input_salario_liquido.get()

    #         # Verifica se o valor é numerico
    #         if sb.isnumeric() and sl.isnumeric():
    #             nome_sheet = "dados_gerais" # nome da planilha
    #             range_dg = "A2:B15"  # range que contém as infos
    #             dados_gerais = [
    #                 ["salario_bruto", int(sb)],
    #                 ["salario_liquido", int(sl)]
    #             ]
    #             self.gsheet.update_sheet(nome_sheet, range_dg, dados_gerais) # Faz a atualização na sheet
    #             popup.destroy() # Fecha a janela de inserção
    #             self.frame_base.pack_forget() # Destroy o pacote da tela base
    #             self.base_frame() # recarrega tela base novamente
    #         else:
    #             messagebox.showerror(title="Salvar dados", message="Digite apenas numeros.")
           

    #     popup = ctk.CTkToplevel(self.window)
    #     popup.title("Atualizar Dados Gerais")
    #     popup.geometry("400x300")
        
    #     # Labels
    #     ctk.CTkLabel(master=popup, text="Atualizar Dados Gerais", font=("Robot", 16)).pack(pady=10)

    #     # Inputs 
    #     input_salario_bruto = ctk.CTkEntry(master=popup, placeholder_text="Valor do Salario Bruto...", width=170)
    #     input_salario_bruto.pack(pady=10)
    #     input_salario_liquido = ctk.CTkEntry(master=popup, placeholder_text="Valor do Salario Liquido..", width=170)
    #     input_salario_liquido.pack(pady=5)


    #     # Buttons
    #     btn_salvar = ctk.CTkButton(master=popup, text="Salvar", fg_color="#FEB403", command=salvar_dados_gerais).pack(side=BOTTOM, pady=10)


    def popup_nova_df(self, acao="novo", valores=None):

        # Para inserção de novo dados em Despesas Fixas

        # Variaveis
        CATEGORIAS = ["Casa", "Assinatura", "Estudos", "Transporte", "Farmacia e Saude", "Outros"]
        FORMA_PAGAMENTO = ["Cartao", "Dinheiro", "Pix", "Boleto"]
        CARTOES = ["None","C6", "Inter", "Itau", "Nubank", "BB"]


        def create_dict_entryctk():
            
            entryctk_data = dict()
            entryctk_data["descricao"] = input_descricao.get()
            entryctk_data["categoria"] = input_categoria.get()
            entryctk_data["valor_total"] = float(input_valor_total.get().replace(",","."))
            entryctk_data["valor_mensal"] = 0
            entryctk_data["status"] = "Nao Pago"
            entryctk_data["forma_pag"] = input_forma_pag.get()
            entryctk_data["cartao"] = input_cartao.get()
            entryctk_data["qtd_meses"] = int(input_meses.get())

            return entryctk_data


        def save():
            
            entryctk_data = create_dict_entryctk()
          
            if (entryctk_data["descricao"] != "" and entryctk_data["valor_total"] != "" and entryctk_data["qtd_meses"] != ""):
                if(isinstance(entryctk_data["valor_total"], (int,float)) and isinstance(entryctk_data["qtd_meses"], (int,float))):
                    month_value = self.calc.division_month(entryctk_data["valor_total"], entryctk_data["qtd_meses"])
                    entryctk_data["valor_mensal"] = round(month_value,2)
                    data = tuple(entryctk_data.values())
                  
                    self.db.set_df_new_data("despesas_fixas", data) # Faz inserção de uma nova despesa
                    popup.destroy() # Fecha a janela de inserção
                    self.frame_df.pack_forget() # Destroy o pacote da tela base
                    self.tela_despesas_fixas() # Chamar a tela para recarregar infos
                else:
                    print("Nao sao numeros...")
            else:
                print("Existem itens em branco....")

        
        def atualizar():
            entryctk_data = create_dict_entryctk()

            if acao == "attdel":
                id = int(valores[0])

            if (entryctk_data["descricao"] != "" and entryctk_data["valor_total"] != "" and entryctk_data["qtd_meses"] != ""):
                if(isinstance(entryctk_data["valor_total"], (int,float)) and isinstance(entryctk_data["qtd_meses"], (int,float))):
                    month_value = self.calc.division_month(entryctk_data["valor_total"], entryctk_data["qtd_meses"])
                    entryctk_data["valor_mensal"] = round(month_value,2)
                    data = tuple(entryctk_data.values())

                    self.db.update_df_data(data, id) # Faz inserção de uma nova despesa
                    popup.destroy() # Fecha a janela de inserção
                    self.frame_df.pack_forget() # Destroy o pacote da tela base
                    self.tela_despesas_fixas() # Chamar a tela para recarregar infos
                else:
                    print("Nao sao numeros...")
            else:
                print("Existem itens em branco....")


        def deletar():
            
            if acao == "attdel":
                id = int(valores[0])
                self.db.delete_df_data(id)
                popup.destroy() # Fecha a janela de inserção
                self.frame_df.pack_forget() # Destroy o pacote da tela base
                self.tela_despesas_fixas() # Chamar a tela para recarregar infos


        if acao == "novo":
            # Criacao da window de nova despesa
            popup = ctk.CTkToplevel(self.window)
            popup.title("Nova Despesa Fixas")
            popup.geometry("400x400")
            
            # Labels
            ctk.CTkLabel(master=popup, text="Nova Despesa Fixa", font=("Robot", 16)).pack(pady=10)

            # Inputs 
            input_descricao = ctk.CTkEntry(master=popup, placeholder_text="Descricao", width=170)
            input_descricao.pack(pady=10)

            input_categoria = ctk.CTkComboBox(master=popup, values=CATEGORIAS, width=170)
            input_categoria.pack(pady=5)

            input_valor_total = ctk.CTkEntry(master=popup, placeholder_text="Valor Total do Gasto", width=170)
            input_valor_total.pack(pady=10)

            input_forma_pag = ctk.CTkComboBox(master=popup, values=FORMA_PAGAMENTO, width=170)
            input_forma_pag.pack(pady=5)

            input_cartao = ctk.CTkComboBox(master=popup, values=CARTOES, width=170)
            input_cartao.pack(pady=5)
                
            input_meses = ctk.CTkEntry(master=popup, placeholder_text="Qtd de meses, minimo 12", width=170)
            input_meses.pack(pady=10)

            # Buttons
            btn_salvar = ctk.CTkButton(master=popup, text="Salvar", fg_color="#FEB403", command=save).pack(side=BOTTOM, pady=10)
        elif acao == "attdel":
            # Criacao da janela para atualizacao de uma despesa fixa
            popup = ctk.CTkToplevel(self.window)
            popup.title("Nova Despesa Fixa")
            popup.geometry("400x450")

            # Inputs
            descricao = StringVar(value=valores[1])
            input_descricao = ctk.CTkEntry(master=popup, placeholder_text="Descricao", width=170, textvariable=descricao)
            input_descricao.pack(pady=10)
            
            input_categoria = ctk.CTkComboBox(master=popup, values=CATEGORIAS, width=170)
            input_categoria.set(valores[2])
            input_categoria.pack(pady=5)

            valor_total = StringVar(value=valores[3])
            input_valor_total = ctk.CTkEntry(master=popup, placeholder_text="Valor Total do Gasto", width=170, textvariable=valor_total)
            input_valor_total.pack(pady=10)

            input_status = ctk.CTkComboBox(master=popup, values=["Nao Pago", "Pago"], width=170)
            input_status.set(valores[5])
            input_status.pack(pady=5)

            input_forma_pag = ctk.CTkComboBox(master=popup, values=FORMA_PAGAMENTO, width=170)
            input_forma_pag.set(valores[6])
            input_forma_pag.pack(pady=5)

            input_cartao = ctk.CTkComboBox(master=popup, values=CARTOES, width=170)
            input_cartao.set(valores[7])
            input_cartao.pack(pady=5)

            input_meses = StringVar(value=valores[8])
            input_meses = ctk.CTkEntry(master=popup, placeholder_text="Qtd de meses, minimo 12", width=170)
            input_meses.pack(pady=10)

            # Buttons
            btn_del = ctk.CTkButton(master=popup, text="Deletar", fg_color="#FEB403", command=deletar).pack(side=BOTTOM, pady=10)
            btn_att = ctk.CTkButton(master=popup, text="Atualizar", fg_color="#FEB403", command=atualizar).pack(side=BOTTOM, pady=10)
            


    def criar_tabela(self, frame, columns, categorias ):

        # Criando cabeçalho da tabela
        tv = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        # tv.place(x=10, rely=.1)

        for i in range(len(categorias)):
            tv.heading(i+1, text=categorias[i])
            tv.column(i+1, anchor="c", width=165)

        style = ttk.Style()
        style.theme_use("default")
    
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])

        return tv    




if __name__ == "__main__":

    app = MainApp()
    app.mainloop()
