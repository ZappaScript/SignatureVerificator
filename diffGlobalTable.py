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
    

    top = 0 
    bot = 99999999   
    
    for key in resultsC:
        #resultsC[key]['FRR'] = (1-resultsC[key]['FRR']) - (1-x[1][key][0])
        #resultsC[key]['FAR'] = (1-resultsC[key]['FAR']) - (1-x[1][key][1])
        print(resultsC[key])
        if(max(resultsC[key]['FRR'],resultsC[key]['FAR']) > top):
            top = max(resultsC[key]['FRR'],resultsC[key]['FAR'])
        if(min(resultsC[key]['FRR'],resultsC[key]['FAR']) < bot):
            bot = min(resultsC[key]['FRR'],resultsC[key]['FAR'])

    ##values = np.arange(float(bot//10-1)*10, float(top//10+2)*10, round(max(abs(float(bot//10-1)*10),float(top//10+1)*10)*0.1,2) )
    values = np.arange(((bot*100)//10*10), (round(top*100//10+1)*10)+10, 10 )
    print(values)
    print(top,bot)
    print((bot//10-1)*10)
    print((top//10+2)*10)
    print(round(max(abs(bot),top)*0.1,2))

    for r in resultsC.keys():
        resultsC[r] = [resultsC[r]["FRR"],resultsC[r]["FAR"]]

    columns = ['ΔFRR','ΔFAR']
    #Data = [ [ ( (x)*100 ) for x in resultsC[row] ] + [ ((x)*100) for x in resultsB[row]] + [ ((x)*100) for x in resultsH[row]] for row in sorted(resultsC.keys()) ] 
    Data = [ [ ( (x)*100 ) for x in resultsC[row] ] for row in sorted(resultsC.keys()) ] 

    print(Data)
    rows = [getName(i) for i in sorted(resultsC.keys())]
    colors = plt.cm.Paired(np.linspace(0, 1, len(rows)))
    n_rows = len(Data)
    index = np.arange(len(columns)) + 0.3
    bar_width = 0.1
    y_offset = np.array([0.0] * len(columns)*3)
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
                        colLabels=columns,
                        loc='bottom',
                        bbox=[0, -0.34, 1.0, 0.3])
    plt.yticks(values , ['%1.2f' % val for val in values])
    plt.xticks([])
   
    plt.title(test.title)
    plt.subplots_adjust(left=0.2, bottom=-0.2)
    plt.savefig(test.saveFile, bbox_inches='tight')
    
    
