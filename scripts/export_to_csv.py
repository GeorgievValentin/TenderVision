import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin@127.0.0.1:5432/tendervision"

engine = create_engine(DATABASE_URL)

query = "SELECT * FROM tenders"
df = pd.read_sql(query, engine)

output_file = "../data/tenders.csv"
df.to_csv(output_file, index = False, encoding = 'utf-8')

print(f"Data was successfully added to {output_file}!")
