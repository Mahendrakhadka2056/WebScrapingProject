import pandas as pd
import requests
from bs4 import BeautifulSoup

class webscraping:
    url = 'https://www.worldometers.info/gdp/nepal-gdp/'
    data = requests.get(url).content
    new_data = BeautifulSoup(data,'html.parser')
    def tableExtract(self):
        table1 = self.new_data.find_all(class_='table-responsive')
        table2 = self.new_data.find_all('td')
        list_of_columns = [x.text.strip() for x in table2]

        td_data = []
        for x in table2[2:]:
            td_data.append(x.get_text(strip=True))

        num_columns = 7
        table_data = [td_data[x:x + num_columns] for x in range(0, len(td_data), num_columns)]
        df = pd.DataFrame([{a: b[i] for i, a in enumerate(list_of_columns)} for b in table_data])
        df.head(30)

ob = webscraping()
ob.tableExtract()




