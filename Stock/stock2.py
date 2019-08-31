import csv
import codecs
import os
import sqlite3
from os import listdir
from os.path import isfile, isdir, join
import gg
import twstock
import time

conn = sqlite3.connect('C:\\GD\\STOCK\\stock.db')
c = conn.cursor()
res = c.execute('select * from v_stock order by ratio desc')
for row in res:
    ls_stock_no = row[0]
    c_mon = conn.cursor()
    res_mon = c_mon.execute( f'select * from v_monthly_revenue t where t.stock_no = "{ls_stock_no}" and t.yyyymm = (select max(yyyymm) from v_monthly_revenue v where v.stock_no = t.stock_no)')
    for row2 in res_mon:
        ls_yyyymm = row2[0]
        lf_current_accu = row2[2]
        lf_last_year_accu_comp = row2[4]
        lf_esp = gg.get_eps(ls_stock_no, 2019, 2)
        lf_esp2 = gg.get_eps(ls_stock_no, 2018, 2)
        lf_esp_ratio = (lf_esp / lf_esp2) * 100
        lf_esp_guess = (lf_esp * 2) * 0.7
        lf_price_guess = lf_esp_guess * 20
        lf_price = row[2]
        lf_price_diff = lf_price_guess - lf_price
    print (f"{ls_stock_no:>6s} 現價:{lf_price:>6.2f} 股利:{row[3]:>6.2f} 殖利率:{row[4] * 100:>6.2f}  {ls_yyyymm:>6s} {lf_current_accu:>20,d} {lf_last_year_accu_comp:>10.2f} EPS:{lf_esp:>6.2f}  Last_EPS:{lf_esp2:>6.2f} {lf_esp_ratio:>6.2f}  預估股利:{lf_esp_guess:>6.2f} 預估股價:{lf_price_guess:>6.2f} 空間:{lf_price_diff:>6.2f} {row[1]:<20s}")