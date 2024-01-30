import customtkinter as ctk
from PIL import Image
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class DespesasVariaveis():

    def __init__(self, window, db, calc, frame_base):
        self.window = window
        self.db = db
        self.calc = calc
        self.frame_base = frame_base
        self.frame_dv = None


    def tela_despesas_variaveis(self):
        
        # Monta o frame novo
        self.frame_base.pack_forget()
        self.frame_dv = ctk.CTkFrame(master=self.window, width=800, height=500, fg_color="white")
        self.frame_dv.pack()

        titulo_area = ctk.CTkLabel(master=self.frame_dv, text=f"Despesas Variaveis", font=("Robot", 20)).place(relx=.5, y=15, anchor="center")

        def voltar_tela():
            self.frame_dv.pack_forget()
            self.frame_base.pack()

        btn_voltar = ctk.CTkButton(master=self.frame_dv, text="Voltar", fg_color="#FEB403", command=voltar_tela).place(relx=.01, rely=.9)


    # def popup_nova_dv(self, acao="novo", valores=None):

    #     # Para inserção de novo dados em Despesas Fixas

    #     # Variaveis
    #     CATEGORIAS = ["Casa", "Assinatura", "Estudos", "Transporte", "Farmacia e Saude", "Outros"]
    #     FORMA_PAGAMENTO = ["Cartao", "Dinheiro", "Pix", "Boleto"]
    #     CARTOES = ["None","C6", "Inter", "Itau", "Nubank", "BB"]


    #     def create_dict_entryctk():
            
    #         entryctk_data = dict()
    #         entryctk_data["descricao"] = input_descricao.get()
    #         entryctk_data["categoria"] = input_categoria.get()
    #         entryctk_data["valor_total"] = float(input_valor_total.get().replace(",","."))
    #         entryctk_data["valor_mensal"] = 0
    #         entryctk_data["status"] = "Nao Pago"
    #         entryctk_data["forma_pag"] = input_forma_pag.get()
    #         entryctk_data["cartao"] = input_cartao.get()
    #         entryctk_data["qtd_meses"] = int(input_meses.get())

    #         return entryctk_data


    #     def save():
            
    #         entryctk_data = create_dict_entryctk()
          
    #         if (entryctk_data["descricao"] != "" and entryctk_data["valor_total"] != "" and entryctk_data["qtd_meses"] != ""):
    #             if(isinstance(entryctk_data["valor_total"], (int,float)) and isinstance(entryctk_data["qtd_meses"], (int,float))):
    #                 month_value = self.calc.division_month(entryctk_data["valor_total"], entryctk_data["qtd_meses"])
    #                 entryctk_data["valor_mensal"] = round(month_value,2)
    #                 data = tuple(entryctk_data.values())
                  
    #                 self.db.set_df_new_data("despesas_fixas", data) # Faz inserção de uma nova despesa
    #                 popup.destroy() # Fecha a janela de inserção
    #                 self.frame_df.pack_forget() # Destroy o pacote da tela base
    #                 self.tela_despesas_fixas() # Chamar a tela para recarregar infos
    #             else:
    #                 print("Nao sao numeros...")
    #         else:
    #             print("Existem itens em branco....")

        
    #     def atualizar():
    #         entryctk_data = create_dict_entryctk()

    #         if acao == "attdel":
    #             id = int(valores[0])

    #         if (entryctk_data["descricao"] != "" and entryctk_data["valor_total"] != "" and entryctk_data["qtd_meses"] != ""):
    #             if(isinstance(entryctk_data["valor_total"], (int,float)) and isinstance(entryctk_data["qtd_meses"], (int,float))):
    #                 month_value = self.calc.division_month(entryctk_data["valor_total"], entryctk_data["qtd_meses"])
    #                 entryctk_data["valor_mensal"] = round(month_value,2)
    #                 data = tuple(entryctk_data.values())

    #                 self.db.update_df_data(data, id) # Faz inserção de uma nova despesa
    #                 popup.destroy() # Fecha a janela de inserção
    #                 self.frame_df.pack_forget() # Destroy o pacote da tela base
    #                 self.tela_despesas_fixas() # Chamar a tela para recarregar infos
    #             else:
    #                 print("Nao sao numeros...")
    #         else:
    #             print("Existem itens em branco....")


    #     def deletar():
            
    #         if acao == "attdel":
    #             id = int(valores[0])
    #             self.db.delete_df_data(id)
    #             popup.destroy() # Fecha a janela de inserção
    #             self.frame_df.pack_forget() # Destroy o pacote da tela base
    #             self.tela_despesas_fixas() # Chamar a tela para recarregar infos


    #     if acao == "novo":
    #         # Criacao da window de nova despesa
    #         popup = ctk.CTkToplevel(self.window)
    #         popup.title("Nova Despesa Fixas")
    #         popup.geometry("400x400")
            
    #         # Labels
    #         ctk.CTkLabel(master=popup, text="Nova Despesa Fixa", font=("Robot", 16)).pack(pady=10)

    #         # Inputs 
    #         input_descricao = ctk.CTkEntry(master=popup, placeholder_text="Descricao", width=170)
    #         input_descricao.pack(pady=10)

    #         input_categoria = ctk.CTkComboBox(master=popup, values=CATEGORIAS, width=170)
    #         input_categoria.pack(pady=5)

    #         input_valor_total = ctk.CTkEntry(master=popup, placeholder_text="Valor Total do Gasto", width=170)
    #         input_valor_total.pack(pady=10)

    #         input_forma_pag = ctk.CTkComboBox(master=popup, values=FORMA_PAGAMENTO, width=170)
    #         input_forma_pag.pack(pady=5)

    #         input_cartao = ctk.CTkComboBox(master=popup, values=CARTOES, width=170)
    #         input_cartao.pack(pady=5)
                
    #         input_meses = ctk.CTkEntry(master=popup, placeholder_text="Qtd de meses, minimo 12", width=170)
    #         input_meses.pack(pady=10)

    #         # Buttons
    #         btn_salvar = ctk.CTkButton(master=popup, text="Salvar", fg_color="#FEB403", command=save).pack(side=BOTTOM, pady=10)
    #     elif acao == "attdel":
    #         # Criacao da janela para atualizacao de uma despesa fixa
    #         popup = ctk.CTkToplevel(self.window)
    #         popup.title("Nova Despesa Fixa")
    #         popup.geometry("400x450")

    #         # Inputs
    #         descricao = StringVar(value=valores[1])
    #         input_descricao = ctk.CTkEntry(master=popup, placeholder_text="Descricao", width=170, textvariable=descricao)
    #         input_descricao.pack(pady=10)
            
    #         input_categoria = ctk.CTkComboBox(master=popup, values=CATEGORIAS, width=170)
    #         input_categoria.set(valores[2])
    #         input_categoria.pack(pady=5)

    #         valor_total = StringVar(value=valores[3])
    #         input_valor_total = ctk.CTkEntry(master=popup, placeholder_text="Valor Total do Gasto", width=170, textvariable=valor_total)
    #         input_valor_total.pack(pady=10)

    #         input_status = ctk.CTkComboBox(master=popup, values=["Nao Pago", "Pago"], width=170)
    #         input_status.set(valores[5])
    #         input_status.pack(pady=5)

    #         input_forma_pag = ctk.CTkComboBox(master=popup, values=FORMA_PAGAMENTO, width=170)
    #         input_forma_pag.set(valores[6])
    #         input_forma_pag.pack(pady=5)

    #         input_cartao = ctk.CTkComboBox(master=popup, values=CARTOES, width=170)
    #         input_cartao.set(valores[7])
    #         input_cartao.pack(pady=5)

    #         input_meses = StringVar(value=valores[8])
    #         input_meses = ctk.CTkEntry(master=popup, placeholder_text="Qtd de meses, minimo 12", width=170)
    #         input_meses.pack(pady=10)

    #         # Buttons
    #         btn_del = ctk.CTkButton(master=popup, text="Deletar", fg_color="#FEB403", command=deletar).pack(side=BOTTOM, pady=10)
    #         btn_att = ctk.CTkButton(master=popup, text="Atualizar", fg_color="#FEB403", command=atualizar).pack(side=BOTTOM, pady=10)
            


    # def criar_tabela(self, frame, columns, categorias ):

    #     # Criando cabeçalho da tabela
    #     tv = ttk.Treeview(frame, columns=columns, show='headings', height=15)
    #     # tv.place(x=10, rely=.1)

    #     for i in range(len(categorias)):
    #         tv.heading(i+1, text=categorias[i])
    #         tv.column(i+1, anchor="c", width=165)

    #     style = ttk.Style()
    #     style.theme_use("default")
    
    #     style.configure("Treeview",
    #                     background="#2a2d2e",
    #                     foreground="white",
    #                     rowheight=25,
    #                     fieldbackground="#343638",
    #                     bordercolor="#343638",
    #                     borderwidth=0)
    #     style.map('Treeview', background=[('selected', '#22559b')])

    #     style.configure("Treeview.Heading",
    #                     background="#565b5e",
    #                     foreground="white",
    #                     relief="flat")
    #     style.map("Treeview.Heading",
    #                 background=[('active', '#3484F0')])

    #     return tv