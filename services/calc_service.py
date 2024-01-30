class CalcService():
    
    def division_month(self, total_value, qtd_months):

        try:
            result = total_value / qtd_months
            return result
        except ZeroDivisionError:
            print("Error: Division by Zero!")

        