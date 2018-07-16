#packages imported
import csv
import subprocess
import re
import sys

#Function to format the urls in the proper cases
#Queries, HTML Trans and direct format supported.
def fformat(oringUrl, destinyUrl):

    #regex validations to make the script compatible with most formats of the origin URL
    #Evaluates if the url has HTTP included
    #HTTPS support soon
    regex = r"^(http|https)://(.*).com\/"
    if re.search(regex, oringUrl):
        oringUrl = re.sub(regex, "/", oringUrl)
    #Evaluates if the url begings with / and add it in case of not including it
    regex = r"/"
    if re.match(regex, oringUrl) == None:
        oringUrl = "/"+oringUrl
    #Evaluates if the line is a query : ?
    if str(oringUrl.find("?")) != "-1":
        #Split the String to make up the special rule.
        OrigUrlBefore,OrigUrlAfter = oringUrl.split("?")
        subprocess.Popen("echo \" if ( \$query_string ~ '"+OrigUrlAfter+"' ) { rewrite '^"+OrigUrlBefore+"?$' "+str(destinyUrl)+"? permanent; } \" >> rules-formatted.inc", shell=True)
        return
    #Evaluates if the line is HTML Trash : ?
    elif str(oringUrl.find("%")) != "-1":
        subprocess.Popen("echo \" if ( \$request_uri ~* '^"+str(oringUrl)+"?$' ) { rewrite . "+str(destinyUrl)+" permanent; } \" >> rules-formatted.inc", shell=True)
        return
    #Formats the rules in the default value.
    subprocess.Popen("echo \"rewrite '^"+str(oringUrl)+"?$' "+str(destinyUrl)+" permanent;\" >> rules-formatted.inc", shell=True)
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
    print ("CSV file formatted")
    print ("The rules were generated in the file: rules-formatted.inc")
    pass

def convertTXT(fileToFormat):
    with open(str(fileToFormat)) as f:
        lines = f.read().split("\n")
        for l in lines:
            urls = str(l).split(",")
            #Remove the blank spaces from the urls before any process
            urls[0] = urls[0].strip()
            urls[1] = urls[1].strip()
            fformat(urls[0],urls[1])
    print ("TXT file formatted")
    print ("The rules generated in the file: rules-formatted.inc")
    pass

#Body of the script
#### ---------------------------------------#####
#################################################
try:
    fileToFormat = sys.argv[1]
except IndexError:
    print ("Please include the file of the rules to be formatted")
    exit()
##################################################################
#validation of the extension of the parameter file so it can decide how to proceed
#the lower function() will leave avoid any issues with the validation of the extension of the file
#for example: m.lower().endswith(('.png', '.jpg', '.jpeg'))
else:
    if str(fileToFormat).lower().endswith('.csv'):
        print ("Formatting the CSV file..."+fileToFormat)
        convertCSV(fileToFormat)
        exit()
    elif str(fileToFormat).lower().endswith('.txt'):
        print ("Formatting the TXT file...")
        convertTXT(str(fileToFormat))
        exit()
    else:
        print ("The extension of the file is not supported")
        exit()
