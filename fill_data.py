import glob
import csv
import pandas as pd
path = 'weather_data/*.csv'
files=glob.glob(path)
import os
weather_list = []
def conv_csv():
    for file in files:
        f=open(file, 'r')
        lines = f.readlines()
        lines1 = [item.replace(" ", ",") for item in lines]
        print lines1
        with open(file,'w') as f1:
            f1.writelines(lines1)
            f1.close()
        f.close()

def rem_dep():
    for file in files:
        f=open(file, 'r')
        lines = f.readlines()
        new_lines = lines[2:]
        add_line =  ["YEAR JAN Rand FEB Rand MAR Rand APR Rand MAY Rand JUN Rand JUL Rand AUG Rand SEPT Rand OCT Rand NOV Rand DEC Rand\n"] + new_lines
        print new_lines
        with open(file,'w') as f1:
            f1.writelines(add_line)
            f1.close()
        f.close()

def rem_extra():
    for file in files:
        f=pd.read_csv(file)
        keep_col = ['YEAR','JAN','FEB', 'MAR', 'APR','MAY','JUN','JUL','AUG','SEPT','OCT','NOV','DEC']
        new_f = f[keep_col]
        new_f.to_csv(file, index=False)

def mod_data():
    df=pd.read_csv('price_data/pepper2014.csv',header=None)
    k=df.apply(set)
    place_list = list(k[0])
    print place_list
    for file in files:
        newfile = file.replace("KARNATAKA_",'')
        os.rename(file,newfile)
months = ['random', ]

def insert_data():
    df=pd.read_csv('price_data/ragi-2014.csv',header=None)
    k=df.apply(set)
    place_list = list(k[0])
    print place_list
    for file in files:
        weather_list.append(file.replace('weather_data/','').replace('.csv',''))
    i=1
    for date in df[1]:
        samp = date.partition('/')[2].rsplit('/', 4)
        month = samp[0]
        df[5][i] = samp[0]
        df[3][i]= samp[0]
        i=i+1;
    print df

# rem_dep()
# conv_csv()
# rem_extra()
# mod_data()
insert_data()