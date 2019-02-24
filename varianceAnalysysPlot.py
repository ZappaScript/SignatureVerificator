import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import matplotlib.patches as mpatches
from auxFuncs import getMethodName
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('results1')
    args.add_argument('results2')
    

    args.add_argument('saveFile')
    args.add_argument('title')
    test = args.parse_args()

    variancesA = json.load(open(test.results1))
    variancesB = json.load(open(test.results2))
   
    Data = [ ]
    Data2 = [ ]
    
    a = [variancesA[result] for result in variancesA ]
    b = [variancesB[result] for result in variancesB ]
    rowName = []
    
    for i in a:
        row = [i[x] for x in i ]
        rowName = [x for x in i]
        Data.append(row)
    
    for i in b:
        row = [i[x] for x in i ]
        
        Data2.append(row)

    columns = [getMethodName(key[:-7]) for key in rowName]
    print(columns)
    print("\n")
    print(Data)
    print("\n")
    ##Data = [ [ ( (x)*100 ) for x in resultsC[row] ] + [ ((x)*100) for x in resultsB[row]] + [ ((x)*100) for x in resultsH[row]] for row in sorted(resultsC.keys()) ] 
    values = np.arange(0,max( [max(i) for i in Data]),50 )
    print(max( [max(i) for i in Data]))


    rows = [key for key in variancesA]
    print(rows)
    colors = plt.cm.Set1(np.linspace(0, 1, len(rows)))
    colors2 = plt.cm.Set3(np.linspace(0, 1, len(rows)))
    n_rows = len(Data)
    index = np.arange(len(columns)) + 0.3
    bar_width = 0.15
    y_offsetA = np.array([0.0] * len(columns))
    y_offsetB = np.array([0.0] * len(columns))
    cell_textA = []
    cell_textB = []
    for row in range(n_rows):
        
        
        a = plt.semilogy(index, Data[row], bar_width, color=colors[row])
        b = plt.semilogy(index+0.1*row, Data2[row], bar_width, color=colors2[row])
        y_offsetA =   Data[row]
        y_offsetB =   Data2[row]
        cell_textA.append(['%1.5f' % (x) for x in y_offsetA])
        cell_textB.append(['%1.5f' % (x) for x in y_offsetB])
    
   
    plt.subplot()
    the_table = plt.table(cellText=cell_textA,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='bottom',
                        bbox=[0, -0.34, 1.0, 0.3])
    
    

    plt.subplot()
    
    the_table2 = plt.table(cellText=cell_textB,
                        rowLabels=rows,
                        rowColours=colors2,
                        colLabels=columns,
                        loc='bottom',
                        bbox=[0, 2*-0.34, 1.0, 0.3])
    

    

    
    
    ##plt.yticks(values , ['%1.2f' % val for val in values])
    plt.xticks([])
    plt.subplots_adjust( bottom=0.4)
    
    plt.savefig(test.saveFile,dpi=300)
    
    
