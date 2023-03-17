import json
import requests
import pandas as pd
'''
資料庫的讀寫函數可以使用 SQLAlchemy，支援 PostgreSQL, MySQL, Oracle,
Microsoft SQL server 等資料庫...
'''
from sqlalchemy import create_engine
 
req = requests.get('http://opendata2.epa.gov.tw/AQI.json')
data = json.loads(req.content.decode('utf8'))
df = pd.DataFrame(data)
 
#透過sqlalchemy模組中的create_engine函數來建立sqlite的連線
#並設定將資料表儲存在memory中(提供一次性的操作使用，若需要永久儲存則可以寫入檔案中)
engine = create_engine('sqlite:///:memory:')
df.to_sql('db_table', engine, index=False)
print(pd.read_sql_query('SELECT `County` as `縣市`, `SiteName` as `區域`, \
    CAST(`PM2.5_AVG` AS int) as `PM2.5` FROM `db_table` \
    order by CAST(`PM2.5_AVG` AS int) ASC', engine))
