from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask import make_response
import numpy as np

app = Flask(__name__)
Bootstrap(app)

#Variables
modbus_objs={'1':'Discrete input', '2':'Coil', '3':'Input register', '4':'Holding register'}
bacnet_objs={'1':'Analog input', '2':'Analog output', '3':'Binary input',
            '4':'Binary output'}
csv_name=''
col_8=1001
csv = ['COV','Name', 'ModBus Addres', 'Data Type', 'Data Format', 'BACnet Object Type', 'BACnet Instance', 'BACnet Unit Group', 'BACnet Object Description']
registros=[]

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    titulo = "TFM"
    if request.method == 'POST':
        render_template('configuracion.html',
                            titulo=titulo)
    else:
        return render_template('index.html',
                           titulo=titulo, csv=csv, texto=registros)
@app.route('/index')
def index():
    global registros, col_8
    col_8=1001
    registros=[]
    titulo = "TFM"
    return render_template('index.html',
                       titulo=titulo, csv=csv)

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    global csv_name
    name= request.form.get('nomCSV', None)
    if name is None:
        name='error'
    else:
        csv_name=name
    return render_template('configuracion.html')

@app.route('/final', methods=['GET', 'POST'])
def final():
    global registros
    global col_8
    col3=request.form['nomBac']
    col5=request.form['dirEsc']
    a=modbus_objs[request.form['optradio']]
    b=bacnet_objs[request.form['optradio1']]
    col6=''
    if(a=='Coil' or a=='Discrete input'):
        col6='Bit'
    else:
        col6='16 Bit Signed Integer'
    col7=b
    col9=request.form['seleccion']
    col10=request.form['descBac']
    nuevo_registro = ['0',col3, str(11), col5, col6, col7, str(col_8), col9, col10]
    if len(registros)<1:
        registros=nuevo_registro
    else:
        registros=np.vstack((registros, nuevo_registro))
    col_8=col_8+1
    return render_template('final.html', name_csv=csv_name, csv=csv, texto=registros)

@app.route('/descarga', methods=['GET', 'POST'])
def descarga():
        global csv
        global registros
        texto_final=''
        for i in csv:
            texto_final+=i+','
        texto_final+='\n'
        if registros[1][0] =='0':
            for i in registros:
                for j in i:
                    texto_final+=j+','
                texto_final+='\n'
        else:
            for j in registros:
                texto_final+=j+','
        response = make_response(texto_final)
        cd = 'attachment; filename='+csv_name+'.csv'
        response.headers['Content-Disposition'] = cd
        response.mimetype='text/csv'
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
