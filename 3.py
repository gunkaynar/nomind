f = open("hugo.txt")



genefinder = {}

for lines in f:
    tokens = lines.split("\t")
    
    if tokens[0].replace(" ","") not in genefinder:
        genefinder[tokens[0].replace(" ","")] = [tokens[0].replace(" ","")]

    
    

    exnames = tokens[1].split(",")
    for exname in exnames:
        if exname.replace(" ","") != '' and exname.replace(" ","") not in genefinder:
            genefinder[exname.replace(" ","")] = [tokens[0]]
        elif exname.replace(" ","") != '' and exname.replace(" ","")  in genefinder:
            genefinder[exname.replace(" ","")].append(tokens[0])
    
    
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
            
f.close()
import sqlite3
            
            

            
            
            
            
            
conn = sqlite3.connect('genefinder.db')
cursor = conn.cursor()
            

try:
	cursor.execute("DROP TABLE records");
except:
	print("No previous data to delete")
            

cursor.execute("""CREATE TABLE records(`gene` text, `symbol` text)""")
for genenames in genefinder:
    for genename in genefinder[genenames]:
        A = genenames
        B = genename
        cursor.execute("INSERT INTO records VALUES (?,?)",(A,B,));
        print("({}) ({})".format(A,B));
            
conn.commit()

            
cursor.execute("SELECT * FROM records WHERE gene=?",("ZNF742",));
row = cursor.fetchall();
for rows in row:
    print("e: {}".format(rows[0]));
    print("s: {}".format(rows[1]));    
            