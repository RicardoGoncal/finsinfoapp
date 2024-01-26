
import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "15eog9iPiQ20kj-RoKqd5U8Q4hXcGvca-RT9XmRoV0pE"

class GSheets():
    
    def login(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPE)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPE
                )

            # delete token for the next run
            # os.remove("E:\\finsinfo\\app\\finsinfoapp\\token.json")
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    

    def setup_inicial(self):
        # Setup Dados Gerais
        nome_sheet = "dados_gerais"
        range_dg = "A2:B15"
        dados_gerais = [
            ["salario_bruto", 0],
            ["salario_liquido", 0]
        ]
        self.update_sheet(nome_sheet, range_dg, dados_gerais)

        # Setup despesas_fixas
        sheet_dpf = "despesas_fixas"
        range_dpf = "A1"
        campos_dpf = [
            ["Descricao","Categoria","Valor_Total","Valor_Mensal","Status","Forma_Pagamento","Qual_Cartao","Qtd_Meses"],
        ]
        self.update_sheet(sheet_dpf, range_dpf, campos_dpf)

        # Setup despesas_variaveis
        sheet_dpv = "despesas_variaveis"
        range_dpv = "A1"
        campos_dpv = [
            ["Descricao","Categoria","Valor_Total","Valor_Mensal","Qual_Cartao","Parcelas","Parcelas_Pagas","Parcelas_Rest"],
        ]
        self.update_sheet(sheet_dpv, range_dpv, campos_dpv)



    def coletar_infos_range(self, nome_sheet, range_sheet):

        service = build('sheets', 'v4', credentials=self.login())
        criar_range = str(nome_sheet)+"!"+str(range_sheet)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=criar_range).execute()
        
        valores = result.get('values',[])
        
        return valores
    

    
    def update_sheet(self, nome_sheet, sheet_range, dados):

        service = build('sheets', 'v4', credentials=self.login())
        sheet = service.spreadsheets()
        criar_range = str(nome_sheet)+"!"+str(sheet_range)

        update = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         range=criar_range, valueInputOption="RAW",
                                         body={"values": dados}).execute()


    def append_sheet(self, nome_sheet, sheet_range, dados):

        service = build('sheets', 'v4', credentials=self.login())
        sheet = service.spreadsheets()
        criar_range = str(nome_sheet)+"!"+str(sheet_range)

        update = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         range=criar_range, valueInputOption="RAW",
                                         body={"values": dados}).execute()
        
    
    def deletar_linha_sheet(self, nome_sheet, sheet_range):
        
        service = build('sheets', 'v4', credentials=self.login())
        sheet = service.spreadsheets()
        criar_range = str(nome_sheet)+"!"+str(sheet_range)

        update = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=criar_range).execute()




if __name__ == "__main__":

    teste = GSheets()
    # teste.setup_inicial()
    r = teste.deletar_linha_sheet(nome_sheet="despesas_fixas",sheet_range="A5:H5")
    # r = teste.coletar_infos_range(nome_sheet="dados_gerais",range_sheet="A1:B10")

    print(r)