import pandas as pd
from math import sqrt
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot
import numpy
import os
from glob import glob

folders = glob("../data/*/")

for folder in folders:
    main_folder = folder + 'output/*'
    print main_folder
    files = glob(main_folder)
    for file in files:
        print file
        l = ["year","price"]
        with open(file, 'r') as data_file:
            lines = data_file.readlines()
            lines[0]= ",".join(l)+"\n" # replace first line, the "header" with list contents
            with open(file, 'w') as out_data:
                for line in lines: # write updated lines
                    out_data.write(line)
