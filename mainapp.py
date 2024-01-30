import customtkinter as ctk
from PIL import Image
from tkinter import *
from tkinter import ttk
from services.db_service import DBService
from services.calc_service import CalcService
from services.setup_app import Setup
from configparser import ConfigParser
from telas.tela_despesas_fixas import DespesasFixas
from telas.tela_despesas_variaveis import DespesasVariaveis
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
        btn_despesas_variaveis = ctk.CTkButton(master=self.frame_base, text="Despesas Variaveis", fg_color="#FEB403", command=self.tela_despesas_variaveis).place(x=10, y=120)
        btn_limite_gastos_categoria = ctk.CTkButton(master=self.frame_base, text="Lim. Categorias", fg_color="#FEB403").place(x=10, y=170)
        btn_atual_dados_gerais = ctk.CTkButton(master=self.frame_base, text="Atual. Dados Gerais", fg_color="#FEB403", command=self.popup_dados_gerais).place(x=10, y=220)

        # Acrescenta Widgets de Label no frame
        salario_bruto_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Bruto: R$ {salario_bruto}", font=("Robot", 16)).place(x=10, y= 10)
        salario_liquido_label = ctk.CTkLabel(master=self.frame_base, text=f"Salario Liquido: R$ {salario_liquido}", font=("Robot", 16)).place(x=200, y= 10)


    def popup_dados_gerais(self):

        def salvar_dados_gerais():
            # Coleta as infos do EntryCTk
            sb_float = float(input_salario_bruto.get().replace(",", "."))
            sl_float = float(input_salario_liquido.get().replace(",", "."))

            # Verifica se o valor é numerico
            if(isinstance(sb_float, (int,float)) and isinstance(sl_float, (int,float))):
                data = tuple([sb_float,sl_float])
                
                self.db.update_geral_data(data, 1)
                popup.destroy() # Fecha a janela de inserção
                self.frame_base.pack_forget() # Destroy o pacote da tela base
                self.base_frame() # recarrega tela base novamente
            else:
                messagebox.showerror(title="Salvar dados", message="Digite apenas numeros.")
           

        popup = ctk.CTkToplevel(self.window)
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
    

    def tela_despesas_fixas(self):

        frame = DespesasFixas(self.window, self.db, self.calc, self.frame_base).tela_despesas_fixas()


    def tela_despesas_variaveis(self):

        frame = DespesasVariaveis(self.window, self.db, self.calc, self.frame_base).tela_despesas_variaveis()



        
if __name__ == "__main__":

    app = MainApp()
    app.mainloop()
