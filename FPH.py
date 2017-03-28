##=========================================####
##                                                Config                                                 ####
##=========================================####


path = "/home/user/Downloads/CaseStudySystems_java"
pathSoot = "/home/user/workspace/soot-types/"
outputPath = "/home/user/Documents/FPH"

##=========================================####
##                                               Imports                                                ####
##=========================================####

import sys
import re
import time
import os

##=========================================####
##                               Auxiliary functions                                                ####
##=========================================####

def prepareFiles(suffix):
    try:
        os.remove("interactions"+suffix+".txt")
    except OSError:
        pass

    try:
        os.remove("summaryPerPair"+suffix+".txt")
    except OSError:
        pass


def processFile(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines

def processLines(lines):
    numFeatures = int(lines[0])
    currIndex = 1
    features = dict()
    baseFeature = None
    for i in range(numFeatures):
        featureName = lines[currIndex].strip()
        if not baseFeature:
            baseFeature = featureName
        currIndex += 1
        print "processing feature", featureName
        numFragments = int(lines[currIndex])
        currIndex += 1
        fragments = dict()
        for f in range(numFragments):
            fwhere = lines[currIndex].strip()
            fwhere = fwhere[:fwhere[:fwhere.rfind(",")].rfind(",")]
            currIndex += 1 
            methodName = lines[currIndex].strip()
            currIndex += 1
            fragmentType = lines[currIndex].strip()
            currIndex += 1
            bp = lines[currIndex].strip() == "true"
            currIndex += 1

            relFragmentTypes = ["MethodDecl", "FieldDecl"]
            irrelFragmentTypes = ["ImportDeclaration", "ImplementsList", ".jpg-Content"
                                  , "InitializerDecl", ".txt-Content", "ClassOrInterface2"]
            irrelFragmentTypes += ["ConstructorDecl"] #still don't know how to handle this
            if (fragmentType in relFragmentTypes):
                fragments[f] = {"where": fwhere, "type": fragmentType, 
                                "methodName": methodName, "bp": bp}
            elif featureName != baseFeature and fragmentType not in irrelFragmentTypes:
                print "fragmentType", fragmentType, "is it important??"
                sys.exit(0)
        if featureName != baseFeature:
            features[featureName] = fragments
        else:
            base = fragments
        currIndex += 1
    return features, base

## assuming everything is a method for now; revise for the case of fields
def analyzeCommutativity(suffix, features, classpathSoot, skipTopFolder, fromSPLVerifier, pathSoot):
    total_start_time = time.time()
    countRWChecks = 0
    numPairsDiffPlace = 0
    numPairsNotBP = 0
    numPairsRW = 0
    pairsRW = ""
    for f1 in features:
        for f2 in features:
            if f1 >= f2:
                continue
            start_time = time.time()
            print f1, f2
            interactionFound = False
            
            for frag1 in features[f1]:
                for frag2 in features[f2]:
                    if features[f1][frag1]["where"] == features[f2][frag2]["where"]:
                        if not features[f1][frag1]["bp"] or not features[f2][frag2]["bp"]:
                            #print features[f1][frag1]
                            #print features[f2][frag2]
                            numPairsNotBP +=1
                            interactionFound = True
                            print "interaction", f1, f2, features[f1][frag1]["methodName"], "not bp"
                            with open("interactions" + suffix + ".txt", "a") as myFile:
                                myFile.write(f1 + "\t" + f2 + "\t" 
                                             + features[f1][frag1]["methodName"] 
                                             + "\tnot bp\n")
                    
                        else:
                            numPairsRW += 1
                            pairsRW += "[" + f1 + "," + f2 + "]"
                            print "here check variables", f1, f2, features[f1][frag1]["methodName"]
                            countRWChecks += 1
                            
                            print features[f1][frag1]["where"]
                            classFile = re.search(r"\W(\w+).java\s*\(\Java-File\)", features[f1][frag1]["where"])
                            classFile = classFile.group(1)
                            #print "classFile", classFile
                            folders = re.findall(r"\W(\w+)\s*\(\Folder\)", features[f1][frag1]["where"])
                            if skipTopFolder:
                                #print "skipping top folder from ", ".".join(folders)
                                folders = folders[:-1]
                                #print "result is: ", ".".join(folders)
                            folders = folders[::-1]
                            folders = ".".join(folders)
                            if (folders):
                                className = folders + "." + classFile
                            else:
                                className = classFile
                            #print className
                            methodName = features[f1][frag1]["where"][:features[f1][frag1]["where"].index("(")]
                            #print methodName
                            #x=raw_input()
                            
                            
                            #only to measure the number of checks
                            #resultCheckVarsRW = False
                            resultCheckVarsRW = checkVarsRW(suffix, classpathSoot, className, methodName, f1, f2, fromSPLVerifier, pathSoot)
                        
                            interactionFound = interactionFound or resultCheckVarsRW
                            #return False
                    else:
                        numPairsDiffPlace += 1
            with open("summaryPerPair" + suffix + ".txt", "a") as myFile:
                myFile.write(f1 + "\t" + f2 + "\t" + str(interactionFound) 
                             + "\t" + str(time.time() - start_time) + "\n")

    with open("summaryPerPair" + suffix + ".txt", "a") as myFile:
        myFile.write("total time\t" + str(time.time() - total_start_time) + "\t" + str(countRWChecks) + "\n")
    print "Commutativity check finished"
    
    
    with open("numChecks.txt", "a") as myFile:
        myFile.write(suffix + "\t" + str(numPairsDiffPlace) + "\t" + str(numPairsNotBP)
                     + "\t" + str(numPairsRW) + "\t" + pairsRW + "\n")
    #return True

def analyzeFeatures(suffix, features, classpathSoot, skipTopFolder=False, fromSPLVerifier=True, pathSoot):
    return analyzeCommutativity(suffix, features, classpathSoot, skipTopFolder, fromSPLVerifier, pathSoot)

def checkVarsRW(suffix, classpathSoot, className, methodName, F1Name, F2Name, fromSPLVerifier, pathSoot):
    oldPath = os.getcwd()
    print "current directory", oldPath
    os.chdir(pathSoot)
    print "entering", pathSoot
    jarSoot = "soot-types.jar"
    splVerif = "T" if fromSPLVerifier else "F"
    cmdLine = "java -jar {} {} {} {} {} {} {} 2>&1 > outputSoot{}".format(jarSoot, classpathSoot,  
                                                                    className, methodName,
                                                                    F1Name, F2Name, splVerif, suffix)
    print "executing", cmdLine
    os.system(cmdLine)
    with open("outputSoot" + suffix, "r") as myFile:
        contentsSoot = myFile.read()
        print contentsSoot

        #Interaction: java.lang.String
        #v1: r0.<EmailSystem.Email: java.lang.String 'to'>
        #v2: r0.<EmailSystem.Client: java.lang.String name>
    os.chdir(oldPath)
    print "back to", oldPath
    
    if "analysis finished" not in contentsSoot:
        raise Exception("there was some problem analyzing r/w variables")

    if "Interaction:" in contentsSoot:
        interactionInfo = contentsSoot[contentsSoot.index("v2: "): ].strip()
        with open("interactions" + suffix + ".txt", "a") as myFile:
            myFile.write(F1Name + "\t" + F2Name 
                         + "\t" + className + "\t" + methodName + "\t" + interactionInfo
                         + "\n")
    
    if "Interaction" in contentsSoot:
        print "interaction vars r/w"
        return True
    
    return False

##=========================================####
##                                                Main script                                          ####
##=========================================####


with open("timeTaken.txt", "a") as myFile:
    myFile.write("Start again" + "\t" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

with open("numChecks.txt", "a") as myFile:
    myFile.write("Start again" + "\t" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

for dirName, subdirList, fileList in os.walk(path, topdown=False):
    if "src/" in dirName:
        continue
    if "src" not in dirName:
        continue
    
    
    print('Found directory: %s' % dirName)

    os.chdir(outputPath)
    
    found = re.search("/(\w+)/src", dirName)
    assert re.search
    system = found.group(1)

    suffix = "_" + system
    prepareFiles(suffix)

    pathWithoutSrc = dirName[:dirName.rfind("/")]
    filesInDir =  os.listdir(pathWithoutSrc)
    filesTxt = [f for f in filesInDir if f.endswith(".txt")]
    assert len(filesTxt) == 1
    
    filename = filesTxt[0]
    print "will use", filename
    
    lines = processFile(pathWithoutSrc + "/" + filename)
    features, base = processLines(lines)

    classpathSoot = pathWithoutSrc + "/bin"
    
    skipTopFolder = "gpl" in pathWithoutSrc
    fromSPLVerifier = "splverifier" in pathWithoutSrc

    analyzeFeatures(suffix, features, classpathSoot, skipTopFolder, fromSPLVerifier, pathSoot)
    
    with open("summaryPerPair" + suffix + ".txt", "r") as myFile:
        lineTime = myFile.readlines()[-1]
    
    print "timeTaken: ", lineTime
    
    with open("timeTaken.txt", "a") as myFile:
        myFile.write(suffix + "\t" + str(len(features)) + "\t" + lineTime)
    
    print "finished one"
    #raw_input()


