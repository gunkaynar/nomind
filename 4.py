f = open("hugo.txt")





            
import sqlite3












            
conn = sqlite3.connect('symbol.db')
cursor = conn.cursor()



try:
	cursor.execute("DROP TABLE records");
except:
	print("No previous data to delete")
            
cursor.execute("""CREATE TABLE records(`symbol` text, `ncbi` text,'ensembl' text)""")
for line in f:
    tokens = line.split("\t")
    A = tokens[0].replace(" ","")
    B = tokens[3].replace(" ","")
    C=  tokens[4].replace("\n","")
    cursor.execute("INSERT INTO records VALUES (?,?,?)",(A,B,C,));
    print("({}) ({}) ({})".format(A,B,C));
            
conn.commit()
            










f.close()



