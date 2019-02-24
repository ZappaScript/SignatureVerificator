import numpy as np
import matplotlib.pyplot as plt
import argparse
import json

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('resultsC')
    args.add_argument('resultsC2')
    args.add_argument('resultsB')
    args.add_argument('resultsB2')
    args.add_argument('resultsH')
    args.add_argument('resultsH2')
    

    args.add_argument('saveFile')
    args.add_argument('title')
    test = args.parse_args()

    resultsC = json.load(open(test.resultsC))
    resultsB = json.load(open(test.resultsB))
    resultsH = json.load(open(test.resultsH))
    resultsC2 = json.load(open(test.resultsC2))
    resultsB2 = json.load(open(test.resultsB2))
    resultsH2 = json.load(open(test.resultsH2))
    

    top = 0 
    bot = 99999999   
    for x in [(resultsC,resultsC2),(resultsB,resultsB2),(resultsH,resultsH2)]:
        for key in x[0]:
            x[0][key][0] = (1-x[0][key][0]) - (1-x[1][key][0])
            x[0][key][1] = (1-x[0][key][1]) - (1-x[1][key][1])
            if(max(x[0][key][0],x[0][key][1]) > top):
                top = max(x[0][key][0],x[0][key][1])
            if(min(x[0][key][0],x[0][key][1]) < bot):
                bot = min(x[0][key][0],x[0][key][1])

    ##values = np.arange(float(bot//10-1)*10, float(top//10+2)*10, round(max(abs(float(bot//10-1)*10),float(top//10+1)*10)*0.1,2) )
    values = np.arange(((bot*100)//10*10), (round(top*100//10+1)*10)+10, 10 )
    print(values)
    print(top,bot)
    print((bot//10-1)*10)
    print((top//10+2)*10)
    print(round(max(abs(bot),top)*0.1,2))

    
    columns = ['ΔFRR','ΔFAR']
    Data = [ [ ( (x)*100 ) for x in resultsC[row] ] + [ ((x)*100) for x in resultsB[row]] + [ ((x)*100) for x in resultsH[row]] for row in sorted(resultsC.keys()) ] 
    


    rows = [i for i in sorted(resultsC.keys())]
    colors = plt.cm.Paired(np.linspace(0, 1, len(rows)))
    n_rows = len(Data)
    index = np.arange(len(columns)*3) + 0.3
    bar_width = 0.1
    y_offset = np.array([0.0] * len(columns)*3)
    cell_text = []
    ##for it,row in enumerate(sorted(resultsC.keys())):
    for row in range(n_rows):
        
        ##plt.bar(index, resultsC[row][0], bar_width, bottom=resultsC[row][0], color=colors[it])
        ##
        ##plt.bar(index, resultsC[row][1], bar_width, bottom=resultsC[row][1], color=colors[it])

        ##plt.bar(index, resultsB[row][0], bar_width, bottom=resultsB[row][0], color=colors[it])
    
        ##plt.bar(index, resultsB[row][1], bar_width, bottom=resultsB[row][1], color=colors[it])

        ##plt.bar(index, resultsH[row][0], bar_width, bottom=resultsH[row][0], color=colors[it])
        ##
        ##plt.bar(index, resultsH[row][1], bar_width, bottom=resultsH[row][1], color=colors[it])
        ##
        ##
        ####y_offset = resultsC[row]
        ##print(resultsC[row])
        ##print(y_offset)
        ##rowText = [ (x*100) for x in resultsC[row]] + [ (x*100) for x in resultsB[row]] + [ (x*100) for x in resultsH[row]]
        ##cell_text.append(rowText)
        ##barWidth =(bar_width/6)*0.95**row
        ##toDisplay = sorted(Data[row])
        plt.bar(index+0.1*row, Data[row], bar_width, bottom=0, color=colors[row])
        y_offset =   Data[row]
        cell_text.append(['%1.1f' % (x) for x in y_offset])
    
    header_0 = plt.table(cellText=[['']*3],
                     colLabels=['CEDAR','Bengali','Hindi'],
                     loc='bottom'
                     )
    the_table = plt.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns*3,
                        loc='bottom',
                        bbox=[0, -0.34, 1.0, 0.3])
    plt.yticks(values , ['%1.2f' % val for val in values])
    plt.xticks([])
   
    plt.title(test.title)
    plt.subplots_adjust(left=0.2, bottom=-0.2)
    plt.savefig(test.saveFile, bbox_inches='tight')
    
    
