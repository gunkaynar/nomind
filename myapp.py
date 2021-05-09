from flask import Flask, request, render_template, Response
app = Flask(__name__ ,static_url_path = "", static_folder = "static")
import re
import csv


class PrefixMiddleware(object):
#class for URL sorting 
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        #in this line I'm doing a replace of the word flaskredirect which is my app name in IIS to ensure proper URL redirect
        if environ['PATH_INFO'].lower().replace('/nomind','').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/nomind','')[len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])            
            return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/web')
f = open("hugo.txt",encoding="utf8")
genefinder = {}
symbolfinder = {}
for lines in f:
    tokens = lines.split("\t")
    
    symbolfinder[tokens[0]] = [tokens[0].replace(" ",""), tokens[3].replace(" ",""), tokens[4].replace("\n","")]
    
    
    
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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def homebutton():
    return render_template('home.html')

	
@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/tool', methods =['GET','POST'])
def tool():
    
    ran = []
    prob = []
    genep = []
    geneb = []
    symboln = []
    link=""
    if request.method == 'POST':
        genelist = request.form.get('gene')
        download = request.form.get('down')
        nom = request.form.get('nom')
        inc = request.form.get('inc')
        if genelist=='' or nom==None:
            return render_template('tool_error.html',error='Insufficient input')
        else:
            genes = genelist.split()
            for gene in genes:
                gene = re.sub(r"\s+", "", gene, flags=re.UNICODE)
                if gene not in genefinder :
                    genep.append(gene)
                    prob.append("Gene not found")
                    symboln.append("None")
                    ran.append('-')
                    geneb.append(gene)
                else:
                    realnames = []
                    for row in genefinder[gene]:
                        realnames.append(row)
                    if len(realnames)<=1:
                        for items in realnames:
                            if nom=='ncbi':
                                if symbolfinder[items][1]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)
                                    genep.append(gene)
                                    prob.append("NCBI format not found")
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(symbolfinder[items][1])
                                    geneb.append(gene)

                            elif nom=='ensemble':
                                if symbolfinder[items][2]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)

                                    prob.append("Ensembl format not found")
                                    genep.append(gene)
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(symbolfinder[items][2])
                                    geneb.append(gene)

                            elif nom=='symbol':
                                if symbolfinder[items][0]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)

                                    genep.append(gene)
                                    prob.append("Symbol format not found")
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(symbolfinder[items][0])
                                    geneb.append(gene)
                    elif len(realnames)>1:
                        if inc=="inc":
                            geneb.append(gene)
                            ran.append("*")
                        for items in realnames:
                            symboln.append(items)
                            genep.append(gene)
                            if nom=='ncbi':
                                if symbolfinder[items][1]=='':
                                    prob.append('NCBI format not found')
                                else:
                                    prob.append("Multiple outputs: " + symbolfinder[items][1])
                            elif nom=='ensemble':
                                if symbolfinder[items][2]=='':
                                    prob.append('Ensembl format not found')
                                else:
                                    prob.append("Multiple outputs: " + symbolfinder[items][2])
                            elif nom=='symbol':
                                if symbolfinder[items][0]=='':
                                    prob.append('Not found')
                                else:
                                    prob.append("Multiple outputs: " + symbolfinder[items][0])
            if download=="yes":
                csvdata = [geneb,ran]
                with open("file.csv","w",newline='',encoding="utf8") as f:
                        writer = csv.writer(f)
                        writer.writerows(zip(*csvdata))
                        link ="Download"
            return render_template('result_tool.html', genem=ran,symboln=symboln, geneb=geneb,prob=prob, genep=genep,nomination = nom.upper(),link=link)
    return render_template('tool.html')



@app.route("/download")
def download():
    with open("file.csv") as fp:
         csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Output.csv"})

if __name__ == '__main__':
    app.run(port=8000)