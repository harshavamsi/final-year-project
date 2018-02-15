import glob
import csv
import pandas as pd
import os.path
import re
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

months = ['random','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEPT','OCT','NOV','DEC']

def insert_data():
    df=pd.read_csv('price_data/Ragi2016 - Sheet1.csv',header=None)
    k=df.apply(set)
    place_list = list(k[0])
    print place_list
    for file in files:
        weather_list.append(file.replace('weather_data/','').replace('.csv',''))
    i=1
    for date in df[1]:
        print date
        samp = date.partition('/')[2].rsplit('/', 4)
        if samp[:1][0][:1] == '0':
            month = int(samp[:1][0][1:2])
        else:
            month = samp[:1][0]
        year = 3
        dist = df[0][i]
        print dist
        if dist != 16:
            dist_file = 'weather_data/' + dist+'.csv'
        new_df = pd.read_csv(dist_file,header=None)
        if month:
            new_month = int(month)
            df[4][i] = new_month
            df[3][i] = new_df[new_month][5]
            df[5][i] = year
            if df[0][i] == 'Bangalore':
                df[0][i] = 1
            elif df[0][i] == 'Belgaum':
                df[0][i] = 2
            elif df[0][i] == 'Bellary':
                df[0][i] = 3
            elif df[0][i] == 'Chamrajnagar':
                df[0][i] = 4
            elif df[0][i] == 'Chikmagalur':
                df[0][i] = 5
            elif df[0][i] == 'Chitradurga':
                df[0][i] = 6
            elif df[0][i] == 'Davangere':
                df[0][i] = 7
            elif df[0][i] == 'Dharwad':
                df[0][i] = 8
            elif df[0][i] == 'Gadag':
                df[0][i] = 9
            elif df[0][i] == 'Hassan':
                df[0][i] = 10
            elif df[0][i] == 'Haveri':
                df[0][i] = 11
            elif df[0][i] == 'Kolar':
                df[0][i] = 12
            elif df[0][i] == 'Mandya':
                df[0][i] = 13
            elif df[0][i] == 'Mysore':
                df[0][i] = 14
            elif df[0][i] == 'Shimoga':
                df[0][i] = 15
            elif df[0][i] == 'Tumkur':
                df[0][i] = 16
        if i < 2185:
            i=i+1;
    df.drop(df.columns[[1]], axis=1, inplace=True)
    print df
    df.to_csv('price_data/ragi-final-2016.csv', encoding='utf-8', index=False)
# rem_dep()
# conv_csv()
# rem_extra()
# mod_data()
insert_data()