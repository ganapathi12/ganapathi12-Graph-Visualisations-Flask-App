from flask import Flask, send_file, url_for,render_template, flash, request, redirect
from flask import *  
import graphs
import os
import time
from mako.template import Template

app = Flask(__name__)
app.secret_key = "abc"  

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST','GET'])
def page0():
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
    return render_template('index.html')

@app.route('/processing', methods = ['POST'])  
def success():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            if(request.files['file']):
                f.save(f.filename)
                flash("File Uploaded Sucessfully")
                return  render_template('index2.html')
        else:
            flash("Problem in File uploading")
            return  render_template('index.html')
        
@app.route('/p2', methods = ['POST']) 
def v1():
    if request.method == 'POST':
        n = request.form['nodes']
        v = request.form['val']
        s = request.form['sourse']
        graphs.adjacency(n,v,s)
        graphs.userbfsdraw(n,v,s)
        return render_template('index1.html')
    else:
        return render_template('index.html')
    
@app.route('/page2')
def page2():
    return send_file('usergraph.png', mimetype='image/png')

@app.route('/image2')
def image2():
    return send_file('slowgif.gif', mimetype='image/gif')

@app.route('/list1')
def list1():
    dislist=graphs.adjacencylist()
    #g=0
    #for l in finallist:
     #   print(l[0],"-->",(l[1]))
      #  g+=1
    return render_template('adjacencyuser.html', len = len(dislist), Pokemons = dislist)

@app.route('/list2')
def list2():
    dislist1=[]
    dislist1=graphs.adjacencylist2display()
    return render_template('adjacency.html', len = len(dislist1), Pokemons = dislist1)

@app.route('/page1')
def page1():
    graphs.showgraph()
    return send_file('graphfinal.png', mimetype='image/png')
    #return render_template('graphimage.html')

@app.route('/image1')
def image1():
    graphs.printgraph()
    return send_file('slowgif.gif', mimetype='image/gif')

@app.route('/image3')
def image3():
    graphs.bfsprintgraph()
    return send_file('slowbfs.gif', mimetype='image/gif')

@app.route('/image4')
def image4():
    #graphs.bfsprintgraph()
    return send_file('slowbfs.gif', mimetype='image/gif')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route('/table')
def table():
    rows=graphs.useradj()
#    template = """
#           
#                <table>
#                     % for row in rows:
#                     <tr>
#                          % for cell in row:
#                          <td>${cell}</td>
#                          % endfor
#                     </tr>
#                     % endfor
#                </table>
#        
#    """
    #x=Template(template).render(rows=rows)
    
    return render_template('table.html', len = len(rows), Pokemons = rows)

if __name__ == "__main__":
    app.run(debug=True)
    
    
