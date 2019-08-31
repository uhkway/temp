import csv
import codecs
import os
import sqlite3
from os import listdir
from os.path import isfile, isdir, join
import gg
import twstock
import time
import gg


def csv2db(a_file):
    print(a_file)
    with codecs.open(a_file, 'rb', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'STOCK_NO':
                continue
            time.sleep(1)
            ls_stock_no = row[0]
            print(ls_stock_no)
            ldec_price = float(twstock.realtime.get(ls_stock_no)['realtime']['latest_trade_price'])
            ldec_dividend = gg.get_dividend(ls_stock_no,'2018')
            ldec_ratio = (ldec_dividend / ldec_price)
            c.execute(f"Delete from watch_list where stock_no = '{row[0]}'  ")
            c.execute(f"INSERT INTO watch_list (stock_no,price,dividend,ratio,modify_date,modify_time) \
                  VALUES (  '{ls_stock_no}',{ldec_price},{ldec_dividend},{ldec_ratio},{gg.get_date()},{gg.get_time()})")
            conn.commit()
            print(f"{ls_stock_no} Done!")


my_path = "D:/stock/dividend/"
conn = sqlite3.connect('C:\\GD\\STOCK\\stock.db')
c = conn.cursor()
#files = listdir(my_path)
#for f in files:
#    if f[-3:].upper() == 'CSV':
#        csv2db(my_path+f)
csv2db(r'C:\GD\stock\realtime\stock.csv')
#ls_date = '20190610'
#csv2db(ls_date, my_path + ls_date + '.csv')

print ("Records created successfully")
conn.close()
#print (gg.get_stock_name('1101'))
#print (gg.get_dividend('1101','2018'))
#stock = twstock.realtime.get('1101')
#print(stock['realtime']['latest_trade_price'])