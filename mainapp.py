import customtkinter as ctk
from PIL import Image
from tkinter import *
from tkinter import ttk
from controller.g_sheets import GSheets
from configparser import ConfigParser
from tkinter import messagebox



# Cria a janela do aplicativo
janela = ctk.CTk()

# Iniciar GSheets
gsheet = GSheets()

# Iniciar ConfigParser
config = ConfigParser()

# Classe principal do aplicativo
class MainApp():
    def __init__(self):
        self.janela = janela
        self.gsheet = gsheet
        self.config = config
        self.tema()
        self.tela()
        self.frame_tela_inicial = None
        self.frame_base = None
        self.frame_df = None
        self.tela_inicial()
        janela.mainloop()


    def setup_inicial(self):
        # Criar tabelas com valores padrao no google_sheet
        # config.ini (dados_gerais = 0)
        self.config.read("config.ini")
        cfg_dados_gerais = self.config.get("setup", "dados_gerais")
        if int(cfg_dados_gerais) == 0:
            print("configurando....")
            self.gsheet.setup_inicial()
            self.config.set("setup", "dados_gerais", "1")

            with open('config.ini', 'w') as cfg:
                self.config.write(cfg)
        

    def tema(self):
        ctk.set_appearance_mode("system")


    def tela(self):
        # Configuração da Tela
        self.janela.geometry("800x500")
        self.janela.title("Finsinfo")
        self.janela.resizable(width=False, height=False)

        # Faz o SETUP Inicial
        self.setup_inicial()
        

    def tela_inicial(self):

        # Design da Tela Inicial
        self.frame_tela_inicial = ctk.CTkFrame(master=self.janela, width=800, height=500, fg_color="white")
        self.frame_tela_inicial.pack()
        label_img = ctk.CTkLabel(master=self.frame_tela_inicial, image=PhotoImage(file="./image/logo2.png"), text="").place(x=225, y=75)
        nome_img = ctk.CTkLabel(master=self.frame_tela_inicial, image=PhotoImage(file="./image/nome_programa.png"), text="").place(x=250, y=5)
        entrar_button = ctk.CTkButton(master=self.frame_tela_inicial, text="Entrar", fg_color="#FEB403", command=self.tela_base).place(x=320, y=430)
       
        

    def tela_base(self):
        # Monta o frame novo
        self.frame_tela_inicial.pack_forget()
        self.frame_base = ctk.CTkFrame(master=self.janela, width=800, height=500, fg_color="white")
        self.frame_base.pack()

        # Variaveis para preencher Labels
        dados_gerais = self.gsheet.coletar_infos_range(nome_sheet="dados_gerais",range_sheet="A2:B15")
        for val in dados_gerais:
            if val[0] == "salario_bruto":
                salario_bruto = val[1]

            if val[0] == "salario_liquido":
                salario_liquido = val[1]

        
        # Acrescenta Widgets de Botao no frame
        btn_despesas_fixas = ctk.CTkButton(master=self.frame_base, text="Despesas Fixas", fg_color="#FEB403", command=self.tela_despesas_fixas).place(x=10, y=70)
        btn_despesas_variaveis = ctk.CTkButton(master=self.frame_base, text="Despesas Variaveis", fg_color="#FEB403", command=self.tela_despesas_variaveis).place(x=10, y=120)
        btn_limite_gastos_categoria = ctk.CTkButton(master=self.frame_base, text="Lim. Categorias", fg_color="#FEB403").place(x=10, y=170)
        btn_atual_dados_gerais = ctk.CTkButton(master=self.frame_base, text="Atual. Dados Gerais", fg_color="#FEB403", command=self.popup_dados_gerais).place(x=10, y=220)

        # Acrescenta Widgets de Label no frame
        salario_bruto_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Bruto: {salario_bruto}", font=("Robot", 16)).place(x=10, y= 10)
        salario_liquido_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Liquido: {salario_liquido}", font=("Robot", 16)).place(x=180, y= 10)

    

    def tela_despesas_fixas(self):
        # Monta o frame novo
        self.frame_base.pack_forget()
        self.frame_df = ctk.CTkFrame(master=self.janela, width=800, height=500, fg_color="white")
        self.frame_df.pack()

        titulo_area = ctk.CTkLabel(master=self.frame_df, text=f"Despesas Fixas", font=("Robot", 20)).place(relx=.5, y=15, anchor="center")
        
        def voltar_tela():
            self.frame_df.pack_forget()
            self.frame_base.pack()

        
        def atualizar_item(event):
            item = tabela.identify("item", event.x, event.y)
            valores = tabela.item(item)['values']
            print(valores)
            idd = int(str(tabela.focus()).replace("I", ""))
            self.popup_nova_df(acao="attdel", valores=valores, linha_tabela=idd+1)


        # Area dos botoes
        btn_voltar = ctk.CTkButton(master=self.frame_df, text="Voltar", fg_color="#FEB403", command=voltar_tela).place(relx=.80, rely=.9)
        btn_novo = ctk.CTkButton(master=self.frame_df, text="Novo", fg_color="#FEB403", command=self.popup_nova_df).place(relx=.02, rely=.7)
        btn_atualizar = ctk.CTkButton(master=self.frame_df, text="Atualizar", fg_color="#FEB403").place(relx=.20, rely=.7)
        btn_deletar = ctk.CTkButton(master=self.frame_df, text="Deletar", fg_color="#FEB403").place(relx=.38, rely=.7)


        # Criar tabela
        colunas = (1, 2, 3, 4, 5, 6, 7)
        categorias = ("Descricao","Categoria","Valor Total","Valor Mensal","Status","Forma Pagam.","Cartao")
        tabela = self.criar_tabela(self.frame_df, colunas, categorias)
        tabela.place(x=20, rely=.15)

        # Inserir dados na tabela
        nome_sheet = "despesas_fixas" # nome da planilha
        range_df = "A2:H1000"  # range que contém as infos
        valores_tabela = self.gsheet.coletar_infos_range(nome_sheet, range_df)

        for val in valores_tabela:
            values = (val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7])
            tabela.insert(parent='', index="end", values=values)

        # Deixa o item da tabela com Double Click para abrir as opcoes de deletar ou atualizar
        tabela.bind("<Double-1>", atualizar_item)
        

        
    def tela_despesas_variaveis(self):
        # Monta o frame novo
        self.frame_base.pack_forget()
        self.frame_dv = ctk.CTkFrame(master=self.janela, width=800, height=500, fg_color="white")
        self.frame_dv.pack()

        titulo_area = ctk.CTkLabel(master=self.frame_dv, text=f"Despesas Variaveis", font=("Robot", 20)).place(relx=.5, y=15, anchor="center")

        def voltar_tela():
            self.frame_dv.pack_forget()
            self.frame_base.pack()

        btn_voltar = ctk.CTkButton(master=self.frame_dv, text="Voltar", fg_color="#FEB403", command=voltar_tela).place(relx=.01, rely=.9)


    def popup_dados_gerais(self):

        def salvar_dados_gerais():
            # Coleta as infos do EntryCTk
            sb = input_salario_bruto.get()
            sl = input_salario_liquido.get()

            # Verifica se o valor é numerico
            if sb.isnumeric() and sl.isnumeric():
                nome_sheet = "dados_gerais" # nome da planilha
                range_dg = "A2:B15"  # range que contém as infos
                dados_gerais = [
                    ["salario_bruto", int(sb)],
                    ["salario_liquido", int(sl)]
                ]
                self.gsheet.update_sheet(nome_sheet, range_dg, dados_gerais) # Faz a atualização na sheet
                popup.destroy() # Fecha a janela de inserção
                self.frame_base.pack_forget() # Destroy o pacote da tela base
                self.tela_base() # recarrega tela base novamente
            else:
                messagebox.showerror(title="Salvar dados", message="Digite apenas numeros.")
           

        popup = ctk.CTkToplevel(self.janela)
        popup.title("Atualizar Dados Gerais")
        popup.geometry("400x300")
        
        # Labels
        ctk.CTkLabel(master=popup, text="Atualizar Dados Gerais", font=("Robot", 16)).pack(pady=10)

        # Inputs 
        input_salario_bruto = ctk.CTkEntry(master=popup, placeholder_text="Valor do Salario Bruto...", width=170)
        input_salario_bruto.pack(pady=10)
        input_salario_liquido = ctk.CTkEntry(master=popup, placeholder_text="Valor do Salario Liquido..", width=170)
        input_salario_liquido.pack(pady=5)


        # Buttons
        btn_salvar = ctk.CTkButton(master=popup, text="Salvar", fg_color="#FEB403", command=salvar_dados_gerais).pack(side=BOTTOM, pady=10)


    def popup_nova_df(self, acao="novo", valores=None, linha_tabela=None):

        # Para inserção de novo dados em Despesas Fixas

        # Variaveis
        CATEGORIAS = ["Casa", "Assinatura", "Estudos", "Transporte", "Farmacia e Saude", "Outros"]
        FORMA_PAGAMENTO = ["Cartao", "Dinheiro", "Pix", "Boleto"]
        CARTOES = ["None","C6", "Inter", "Itau", "Nubank", "BB"]


        def criar_dicionario_entryctk():
            
            dados_entryctk = dict()
            dados_entryctk["descricao"] = input_descricao.get()
            dados_entryctk["categoria"] = input_categoria.get()
            dados_entryctk["valor_total"] = float(input_valor_total.get())
            dados_entryctk["valor_mensal"] = 0
            dados_entryctk["status"] = "Nao Pago"
            dados_entryctk["forma_pag"] = input_forma_pag.get()
            dados_entryctk["cartao"] = input_cartao.get()
            dados_entryctk["qtd_meses"] = int(input_meses.get())

            return dados_entryctk


        def salvar():
            
            dados_entryctk = criar_dicionario_entryctk()
          
            if (dados_entryctk["descricao"] != "" and dados_entryctk["valor_total"] != "" and dados_entryctk["qtd_meses"] != ""):
                if(isinstance(dados_entryctk["valor_total"], (int,float)) and isinstance(dados_entryctk["qtd_meses"], (int,float))):
                    nome_sheet = "despesas_fixas" # nome da planilha
                    range_dg = "A2:H1000"  # range que contém as infos
                    valor_mensal = dados_entryctk["valor_total"] / dados_entryctk["qtd_meses"]
                    dados = [
                        [dados_entryctk["descricao"], dados_entryctk["categoria"], str(dados_entryctk["valor_total"]).replace(".", ","), str(valor_mensal).replace(".", ","), 
                         dados_entryctk["status"], dados_entryctk["forma_pag"], dados_entryctk["cartao"], dados_entryctk["qtd_meses"]]
                    ]
                    self.gsheet.append_sheet(nome_sheet, range_dg, dados) # Faz inserção de uma nova despesa
                    popup.destroy() # Fecha a janela de inserção
                    self.frame_df.pack_forget() # Destroy o pacote da tela base
                    self.tela_despesas_fixas() # Chamar a tela para recarregar infos
                else:
                    print("Nao sao numeros...")
            else:
                print("Existem itens em branco....")

        
        def atualizar():
            dados_entryctk = criar_dicionario_entryctk()
          
            if (dados_entryctk["descricao"] != "" and dados_entryctk["valor_total"] != "" and dados_entryctk["qtd_meses"] != ""):
                if(isinstance(dados_entryctk["valor_total"], (int,float)) and isinstance(dados_entryctk["qtd_meses"], (int,float))):
                    nome_sheet = "despesas_fixas" # nome da planilha
                    range_dg = "A{}:H{}".format(linha_tabela,linha_tabela)  # range que contém as infos
                    valor_mensal = dados_entryctk["valor_total"] / dados_entryctk["qtd_meses"]
                    dados = [
                        [dados_entryctk["descricao"], dados_entryctk["categoria"], str(dados_entryctk["valor_total"]).replace(".", ","), str(valor_mensal).replace(".", ","), 
                         dados_entryctk["status"], dados_entryctk["forma_pag"], dados_entryctk["cartao"], dados_entryctk["qtd_meses"]]
                    ]
                    self.gsheet.update_sheet(nome_sheet, range_dg, dados) # Faz inserção de uma nova despesa


                    popup.destroy() # Fecha a janela de inserção
                    self.frame_df.pack_forget() # Destroy o pacote da tela base
                    self.tela_despesas_fixas() # Chamar a tela para recarregar infos
                else:
                    print("Nao sao numeros...")
            else:
                print("Existem itens em branco....")


        def deletar():
            print("Estou deletando a parada....")


        if acao == "novo":
            # Criacao da janela de nova despesa
            popup = ctk.CTkToplevel(self.janela)
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
            btn_salvar = ctk.CTkButton(master=popup, text="Salvar", fg_color="#FEB403", command=salvar).pack(side=BOTTOM, pady=10)
        elif acao == "attdel":
            # Criacao da janela para atualizacao de uma despesa fixa
            popup = ctk.CTkToplevel(self.janela)
            popup.title("Nova Despesa Fixas")
            popup.geometry("400x450")

            # Inputs
            descricao = StringVar(value=valores[0])
            input_descricao = ctk.CTkEntry(master=popup, placeholder_text="Descricao", width=170, textvariable=descricao)
            input_descricao.pack(pady=10)
            
            input_categoria = ctk.CTkComboBox(master=popup, values=CATEGORIAS, width=170)
            input_categoria.set(valores[1])
            input_categoria.pack(pady=5)

            valor_total = StringVar(value=valores[2])
            input_valor_total = ctk.CTkEntry(master=popup, placeholder_text="Valor Total do Gasto", width=170, textvariable=valor_total)
            input_valor_total.pack(pady=10)

            input_status = ctk.CTkComboBox(master=popup, values=["Nao Pago', 'Pago"], width=170)
            input_status.set(valores[4])
            input_status.pack(pady=5)

            input_forma_pag = ctk.CTkComboBox(master=popup, values=FORMA_PAGAMENTO, width=170)
            input_forma_pag.set(valores[5])
            input_forma_pag.pack(pady=5)

            input_cartao = ctk.CTkComboBox(master=popup, values=CARTOES, width=170)
            input_cartao.set(valores[6])
            input_cartao.pack(pady=5)
            
            meses = StringVar(value=valores[7])
            input_meses = ctk.CTkEntry(master=popup, placeholder_text="Qtd de meses, minimo 12", width=170, textvariable=meses)
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
