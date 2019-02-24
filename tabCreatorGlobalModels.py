import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
from auxFuncs import getName
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('resultsC')
   

    args.add_argument('saveFile')
    args.add_argument('title')
    test = args.parse_args()

    resultsC = json.load(open(test.resultsC))
    
    for x in [resultsC]:
        for i in x: 
            x[i] =[1*(1 - x[i][0]),1*(1 - x[i][1])]

    values = np.arange(0, 110, 10)

    columns = ['%FRR','%FAR']
    Data = [[ (x*100) for x in resultsC[row]] for row in sorted(resultsC.keys()) ] 
    print(Data)


    rows = [getName(i) for i in sorted(resultsC.keys())]
    colors = plt.cm.Paired(np.linspace(0, 1, len(rows)))
    n_rows = len(Data)
    index = np.arange(len(columns)) + 0.3
    bar_width = 0.1
    y_offset = np.array([0.0] * len(columns))
    cell_text = []
    
    for row in range(n_rows):
       
        plt.bar(index+0.1*row, Data[row], bar_width, bottom=0, color=colors[row])
        y_offset =   Data[row]
        cell_text.append(['%1.1f' % (x) for x in y_offset])
    
    header_0 = plt.table(cellText=[['']],
                     colLabels=['CEDAR + Bengali + Hindi'],
                     loc='bottom'
                     )
    the_table = plt.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns*3,
                        loc='bottom',
                        bbox=[0, -0.34, 1.0, 0.3])
    plt.yticks(values , ['%d' % val for val in values])
    plt.xticks([])
   
    ##plt.title(test.title)
    #plt.subplots_adjust(left=0.2, bottom=-0.2)
    plt.savefig(test.saveFile, bbox_inches='tight')
    