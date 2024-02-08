import csv
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

class webscraping:
    url = 'https://www.worldometers.info/gdp/nepal-gdp/'
    data = requests.get(url).content
    new_data = BeautifulSoup(data,'html.parser')

    def __init__(self):
        pass
    def tableExtract(self):
        table1 = self.new_data.find_all(class_='table-responsive')
        table2 = self.new_data.find_all('th')
        list_of_columns = [x.text.strip() for x in table2]
        td_tags = self.new_data.find_all('td')
        # to get data into table. assign a list variable and using loop append data in a list
        td_data = []
        for x in td_tags[2:]:
            td_data.append(x.get_text(strip=True))

        # Now add all data into table format
        table_columns = 7
        table_data = [td_data[x:x+table_columns] for x in range(0,len(td_data),table_columns)]
        df = pd.DataFrame([{a:b[i] for i,a in enumerate(list_of_columns)} for b in table_data])

        # Save data into csv file
        fle = 'NepalGDP.xlsx'
        with open(fle,'w',newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(df)

        # insert data into database
        conn = sqlite3.connect('GDP.db')
        cur = conn.cursor()
        query = """ create table GDP(Year int, GDP_Nominal_Current USD int, GDP_Real_Inflation adj int, GDP_change int, GDP_per_capita int, Pop_change int, Population int)"""
        cur.execute(query)
        df.to_sql('GDP',conn,index=False,if_exists='replace')
        conn.commit()
        conn.close()

ob = webscraping()
ob.tableExtract()

class DataExtract(webscraping):
    def __init__(self):
        super().__init__()
    def data(self):
        self.cur.execute('select * from gdp').fetchall()


obj = DataExtract()
obj.data()
