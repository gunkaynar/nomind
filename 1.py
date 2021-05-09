f = open("hugo.txt")
filk = open("hugogenes_entrez.txt")

a= []
for lines in f:
    token = lines.split("\t")
    a.append(token[0])
    synos = token[1].split(",")
    for item in synos:
        a.append(item.replace(" ",""))
    other = token[2].split(",")
    for others in other:
        a.append(others.replace(" ",""))
    
    

inside_new = 0
not_inside_new = 0
for line in filk:
    tokens = line.split("\t")
    if tokens[0].replace("~withdrawn","") in a:
        inside_new += 1
    elif tokens[0].replace("~withdrawn","") not in a:
        not_inside_new += 1
        print(tokens[0])
        
        
        

f.close()
filk.close()