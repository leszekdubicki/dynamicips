from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.script import Server, Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, './dynamicips.sqlite')

#initialize app:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#for wtforms (I think ;) i need to specify secret_key
app.secret_key = "lexosecretkey"
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

#function for creating dictionary from a model.
def dict_model(model):
    M = {}
    keysToRem = []
    for key in model.__dict__:
        try:
            j = jsonify({key: model.__dict__[key]})
        except:
            keysToRem.append(key)
    for key in model.__dict__:
        #add a key:
        if not key in keysToRem: 
            M[key] = model.__dict__[key]
    return M

def argsTuple(argsDictionary, keysOrderTuple):
    #converts Python dictionary into tuple of given order
    argumentsTuple = ()
    for key in keysOrderTuple:
        if key in argsDictionary:
            argumentsTuple = argumentsTuple + (argsDictionary[key],)

#Models Definition:
class Host(db.Model):
    #class for projects record
    #__tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    ip_address = db.Column(db.String(128))
    domain_name = db.Column(db.String(128))
    #key is a host cert public key used to login (it's recommended to use certs with passwords....
    key = db.Column(db.String(1024))
    ssh_port = db.Column(db.Integer)
    description =  db.Column(db.String(512))
    def __init__(self, name, ip_address, domain_name, key, ssh_port, description = ""):
        self.name = name
        self.ip_address = ip_address
        self.domain_name = domain_name
        self.key = key
        self.ssh_port = ssh_port
        self.description = description
    def __repr__(self):
        return "<Host %r>" % self.name
    def json(self, var_name = ''):
        #returns json representation of the model:
        if var_name == '':
            var_name = self.id
        variable = dict_model(self) 
        if '_sa_instance_state' in variable:
            variable.__delitem__('_sa_instance_state')
        return jsonify({var_name:variable})

#webapp routes part:
#define username and password:
@auth.get_password
def get_password(username):
    if username == 'superuser':
        return 'webapi'
    return None

#define response in case of unauthorized access:
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'})

@app.route('/hosts', methods = ['GET'])
@auth.login_required
def get_hosts():
    #return all hosts in db:
    hosts = Host.query.all()
    hostsList = []
    for host in hosts:
        hostsList.append(host.json())
    return jsonify({'hosts':hostsList})

@app.route('/hosts/add', methods = ['POST'])
@auth.login_required
def add_host():
    VAR = request.json['project']
    initFields = ('name', 'ip_address', 'domain_name', 'key', 'ssh_port', 'description')
    args = argsTuple(initFields)
    #h = Host()
    #db.session.add(h)
    return jsonify(args)
"""
#@app.route('/bank/api/v1.0/customers', methods = ['POST'])
@app.route('/bank/api/v1.0/resources/<string:table_name>', methods = ['POST'])
@auth.login_required
def create_resource(table_name):
    record = {}
    if table_name in ["transactions"]:
        #not allowed to edit transactions directly
        return jsonify({'error':'this table can not be modified directly'}), 410
    fields = DB.getFields(table_name)
    for F in fields:
        if F in request.json:
            record[F] = request.json[F]
    record = DB.create(table_name, record)
    return jsonify({DB.recordName(table_name):record}), 201

"""
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
context = ('cert/dynamicip_server.crt', 'cert/dynamicip_server.key')
server = Server(host="0.0.0.0", port=5000, ssl_context=context)
manager.add_command("runserver", server)

if __name__ == "__main__":
    #import ssl
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    
    manager.run()
    #if "start" in sys.argv:
    #    context = ('cert/server.crt', 'cert/server.key')
    #    app.run(host='0.0.0.0', ssl_context=context, debug=True)
