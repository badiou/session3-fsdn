from werkzeug.exceptions import HTTPException
# imprtation de flask
from flask import Flask,render_template,request,redirect,url_for
# importation de SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
#from flask.ext.bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

#pip install Flask-Bootstrap
# creation de l'application Flask
app = Flask(__name__)

# Mise en place de la chaine de connexion à la base de
# données
motdepasse = "B@diou2015"
motdepasse = quote_plus(motdepasse)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{}@localhost:5432/gestion_db".format(
    motdepasse)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creation d'une instance de la base de données
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

class Etudiant(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    adresse = db.Column(db.String(200), nullable=True)
    #pays = db.Column(db.String(200), nullable=True)
    filiere_id = db.Column(db.Integer, db.ForeignKey('filieres.id'),
                          nullable=False)


class Filiere(db.Model):
    __tablename__='filieres'
    id = db.Column(db.Integer, primary_key=True)
    libellefiliere = db.Column(db.String(50), nullable=False)
    etudiants = db.relationship(
        'Etudiant', backref=db.backref('filieres', lazy=True))
    


#db.create_all()
@app.route('/')
def page_accueil():
    return render_template('index.html')

@app.route('/filieres') #1
def liste_filieres():
    filieres=Filiere.query.all() #2 #3
    return render_template('filieres.html',data=filieres) #4

@app.route('/add_filiere',methods=['POST','GET'])
def creation_filiere():
    
    if request.method=='GET':
        return render_template('create.html')
    else:
        libelle=request.form.get('libellefiliere')
        filiere=Filiere(libellefiliere=libelle)
        db.session.add(filiere)
        db.session.commit()
        
        return redirect(url_for('liste_filieres'))
    
@app.route('/filieres/<int:id_filiere>',methods=['POST','GET','DELETE'])
def une_filiere(id_filiere):
    filiere=Filiere.query.get(id_filiere)
    if request.method=='GET':
        return render_template('edit-filiere.html',data=filiere)
    elif request.method=='POST':
        filiere.libellefiliere=request.form.get('libellefiliere')
        db.session.commit()
        return redirect(url_for('liste_filieres'))

@app.route('/etudiants') #1
def liste_etudiants():
    etudiants=Etudiant.query.join(Filiere,Filiere.id==Etudiant.filiere_id).all() #2 #3   
    return render_template('etudiants.html',data=etudiants) #4  


@app.route('/add_etudiant',methods=['POST','GET'])
def creation_etudiant():
    
    if request.method=='GET':
        filieres=Filiere.query.all()
        return render_template('etudiant-create.html',filieres=filieres)
    else:
        nom=request.form.get('nom')
        prenom=request.form.get('prenom')
        adresse=request.form.get('adresse')
        email=request.form.get('email')
        filiere_id=request.form.get('filiere_id')
        etudiant=Etudiant(nom=nom,prenom=prenom,adresse=adresse,email=email,filiere_id=filiere_id)
        db.session.add(etudiant)
        db.session.commit()
        return redirect(url_for('liste_etudiants'))

# les errorhandler permettent de capturer les erreurs
@app.errorhandler(404)
def handle_exception(error):
    return render_template("error_pages/404_error.html",error=error), 404

@app.errorhandler(500)
def handle_exception(error):
    return render_template("error_pages/500_error.html",error=error), 500


if __name__=="main":
    app.run(debug=True)
    
        
        

        

