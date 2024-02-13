from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
class worldmeter:
    url = 'https://www.worldometers.info/gdp/india-gdp/'
    data = requests.get(url).content
    cur = BeautifulSoup(data, 'html.parser')

    def tabledata(self):
        table1 = self.cur.find_all(class_='table-responsive')
        column_1 = self.cur.find_all('th')
        column_2 = [x.text.strip() for x in column_1]  # this variable hold list of columns

        # Now extract row data
        row_data = self.cur.find_all('td')
        row_data1 = []
        for x in row_data[2:]:
            row_data1.append(x.get_text(strip=True))

        column = 7
        row_table = [row_data1[x:x + column] for x in range(0, len(row_data1), column)]
        df = pd.DataFrame([{data: a[i] for i, data in enumerate(column_2)} for a in row_table])

        # Database connectivity
        db = sqlite3.connect('indiaGDP.db')
        cur_ = db.cursor()

        # Create table
        query = """ create table india(Year int, GDP_Nominal_current_USD int,GDP_Real int,GDP_change float,GDP_per_capita int, Pop_change float,Population int) """

        # Insert data in table
        df.to_sql('india', db, index=False, if_exists='replace')
        db.commit()
        db.close()


obj = worldmeter()
obj.tabledata()