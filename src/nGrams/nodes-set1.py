import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015
#example output: format 'node-id,node-attribute,year1,year2,year3... year?'

dictWords = collections.OrderedDict();
dictYears = collections.OrderedDict();
resultFileN = '/results/set1/Nodes-set1.txt';

def parse(resultsPath, dirPath, nodesFileN):
    global dictWords;
    global dictYears;    
    global resultFileN;
    
    print "Beginning program to parse file and create node listings for set1\n"

    resultFileN = resultsPath + resultFileN

    #load word-to-id map
    with open(nodesFileN, 'r') as edgeFile:
        for line in edgeFile:
            vars = line.split(',');
            id = vars[0];
            word = vars[1].strip('\n');
            dictWords[word] =  id; 

    try:
        os.remove(resultFileN);
    except OSError:
        pass;


    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(dirPath, '*')):
        with open(fileN, "r") as file:
            print("Current file: " + file.name)
        
            for line in file:
                args = line.split("\t");
                word = args[0]
                listSize = len(args)

                #add year information for edge occurrence
                for k in range(3, listSize):
                    tok = args[k].split(",")
                    year = int(tok[0])
                    occur = int(tok[1])
               
                    #error checking: don't record words that aren't in nodesDict.txt
                    if not word in dictWords:
                        continue;
                            
                    #add word occurrence to dictionary 
                    if not word in dictYears:
                        dictYears.update({word : [year]});
                    else:
                        if not year in dictYears[word]:
                            dictYears[word].append(year);

    writeRecords();                

def writeRecords():
    resultFile = open(resultFileN, "w");

    for w, yr in dictYears.iteritems():
        idNum = dictWords[w];
        output = str(idNum) + "," + w + "," + ','.join(map(str, yr));
        resultFile.write(output + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide path to results dir, a directory containing txt files to read from and nodes dictionary");
        exit();
    
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    arg3 = sys.argv[3];
    parse(arg1, arg2, arg3);


if __name__ == "__main__":
    main()
