from flask import Flask, request, render_template, Response
app = Flask(__name__ ,static_url_path = "", static_folder = "static")
import sqlite3
import re
import csv


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
    genefinderdb = sqlite3.connect('genefinder.db')
    symboldb = sqlite3.connect('symbol.db')
    cursor1 = genefinderdb.cursor()
    cursor2 = symboldb.cursor()
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
                cursor1.execute("SELECT * FROM records WHERE gene=? ",(gene,));
                rows = cursor1.fetchall();
                if rows == []:
                    genep.append(gene)
                    prob.append("Gene not found")
                    symboln.append("None")
                    ran.append('-')
                    geneb.append(gene)
                else:
                    realnames = []
                    for row in rows:
                        realnames.append(row[1])
                    if len(realnames)<=1:
                        for items in realnames:
                            cursor2.execute("SELECT * FROM records WHERE symbol=? ",(items,));
                            realrow = cursor2.fetchone();
                            if nom=='ncbi':
                                if realrow[1]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)
                                    genep.append(gene)
                                    prob.append("NCBI format not found")
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(realrow[1])
                                    geneb.append(gene)

                            elif nom=='ensemble':
                                if realrow[2]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)

                                    prob.append("Ensembl format not found")
                                    genep.append(gene)
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(realrow[2])
                                    geneb.append(gene)

                            elif nom=='symbol':
                                if realrow[0]=='':
                                    if inc=="inc":
                                        ran.append('-')
                                        geneb.append(gene)

                                    genep.append(gene)
                                    prob.append("Symbol format not found")
                                    symboln.append(realnames[0])
                                else:
                                    ran.append(realrow[0])
                                    geneb.append(gene)

                    elif len(realnames)>1:
                        if inc=="inc":
                            geneb.append(gene)
                            ran.append("*")
                        for items in realnames:
                            symboln.append(items)
                            genep.append(gene)
                            cursor2.execute("SELECT * FROM records WHERE symbol=? ",(items,));
                            realrow = cursor2.fetchone();
                            if nom=='ncbi':
                                if realrow[1]=='':
                                    prob.append('NCBI format not found')
                                else:
                                    prob.append("Multiple outputs: " + realrow[1])
                            elif nom=='ensemble':
                                if realrow[2]=='':
                                    prob.append('Ensembl format not found')
                                else:
                                    prob.append("Multiple outputs: " + realrow[2])
                            elif nom=='symbol':
                                if realrow[0]=='':
                                    prob.append('Not found')
                                else:
                                    prob.append("Multiple outputs: " + realrow[0])
            if download=="yes":
                csvdata = [geneb,ran]
                with open("file.csv","w",newline='') as f:
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
    app.run(debug=False, port=5000)