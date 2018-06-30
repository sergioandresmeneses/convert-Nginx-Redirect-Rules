#packages imported
import csv
import subprocess
import re
import sys

#Function to format the urls in the proper cases
#Queries, HTML Trans and direct format supported.
def fformat(oringUrl, destinyUrl):
    #Evaluates if the line is a query : ?
    if str(oringUrl.find("?")) != "-1":
        print ("Query!!!")
        #Split the String to make up the special rule.
        OrigUrlBefore,OrigUrlAfter = oringUrl.split("?")
        print ( "Before ?: " + OrigUrlBefore)
        print ( "After ?: " + OrigUrlAfter)
        subprocess.Popen("echo \" if ( \$query_string ~ '"+OrigUrlAfter+"' ) { rewrite '^/"+OrigUrlBefore+"/?$' "+str(destinyUrl)+"? permanent; } \" >> rules-formatted.inc", shell=True)
        print("-------------Query-----------------")
        return
    else:
        print ("FAIL Query!!!")
    #Evaluates if the line is HTML Trash : ?
    if str(oringUrl.find("%")) != "-1":
        print ("HTML Trash!!!")
        subprocess.Popen("echo \" if ( \$request_uri ~* '^/"+str(oringUrl)+"/?$' ) { rewrite . "+str(destinyUrl)+" permanent; } \" >> rules-formatted.inc", shell=True)
        print("-------------HTML-----------------")
        return
    else:
        print ("FAIL HTML!!!")

    #Formats the rules in the default value.
    subprocess.Popen("echo \"rewrite '^/"+str(oringUrl)+"/?$' "+str(destinyUrl)+" permanent;\" >> rules-formatted.inc", shell=True)
    pass

def convertCSV(fileToFormat):
    #sys.argv[1] is the file passed as parameter
    #sys.argv[0] is the script itself
    with open (str(fileToFormat)) as f:
        read = csv.reader(f)
        for line in read:
            #Remove the blank spaces from the urls before any process
            line[0] = line[0].strip()
            print ("line0"+str(line[0]))
            line[1] = line[1].strip()
            print ("line1"+str(line[1]))
            fformat(line[0],line[1])
    #Test added only for testing porpuses.
    subprocess.Popen("echo \"------ New Test -----\" >> rules-formatted.inc", shell=True)
    print ("The rules generated in the file: rules-formatted.inc")
    pass


#Body of our script
#### ---------------------------------------#####
#################################################
fileToFormat = sys.argv[1]
#Validation for no files passed as parameters in the Script
if len(sys.argv) != 2:
    print ("Please include the file of the rules to be formatted")
    exit()
elif str(fileToFormat).endswith('.csv'):
    print ("Formatting the CSV file..."+fileToFormat)
    convertCSV(fileToFormat)
    exit()
#elif str(len(sys.argv[1])).endswith('.txt'):
#    print ("Formatting the TXT file...")
    ##NEXT FEATURE
    #convertTXT(len(sys.argv))
#    exit()
#else:
#    print ("The extension of the file is not supported")
#    exit()
