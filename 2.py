f = open("hugo.txt")



genefinder = {}

for lines in f:
    tokens = lines.split("\t")
    
    

    exnames = tokens[1].split(",")
    for exname in exnames:
        if exname.replace(" ","") != '' and exname.replace(" ","") not in genefinder:
            genefinder[exname.replace(" ","")] = [tokens[0]]
        elif exname.replace(" ","") != '' and exname.replace(" ","")  in genefinder:
            genefinder[exname.replace(" ","")].append(tokens[0])
            print(exname)
    
    
    othernames = tokens[2].split(",")
    for othername in othernames:
        if othername.replace(" ","") != '' and othername.replace(" ","") not in genefinder:
            genefinder[othername.replace(" ","")] = [tokens[0]]
        elif othername.replace(" ","") != '' and othername.replace(" ","")  in genefinder:
            genefinder[othername.replace(" ","")].append(tokens[0])
       
    if tokens[3]!="":
        if tokens[3].replace(" ","") not in genefinder:
            genefinder[tokens[3].replace(" ","")] = [tokens[0]]
        elif tokens[3].replace(" ","") in genefinder:
            genefinder[tokens[3].replace(" ","")].append(tokens[0])
    
    if tokens[4]!="\n":
        if tokens[4].replace("\n","") not in genefinder:
            genefinder[tokens[4].replace("\n","")] = [tokens[0]]
        elif tokens[4].replace("\n","") in genefinder:
            genefinder[tokens[4].replace("\n","")].append(tokens[0])
            
            
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            