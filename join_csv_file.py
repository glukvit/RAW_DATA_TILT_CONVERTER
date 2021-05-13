import pandas as pd    
from pathlib import Path

data_dir = Path("/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/min")

df = pd.concat([pd.read_csv(f, compression='gzip') for f in data_dir.glob("*.csv")], ignore_index=True)
df.to_csv("/media/gluk/ca1c79c0-ddfe-428e-8c1a-b57d5bbad96c/EO_CONVERT/ASC/all_1min.csv", index=False)