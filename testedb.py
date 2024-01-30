from services.setup_app import Setup
from services.db_service import DBService


db = DBService()

values = ('teste4', 'teste4', 132.5, 133.8, 'teste4', 'teste4', 'teste4', 0)

db.set_df_new_data("despesas_fixas", values)



