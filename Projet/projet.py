


from flask import Flask, render_template,request,jsonify,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import cx_Oracle
app=Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='oracle://C##project:asma@localhost:1521/orcl'
app.config['SQLAlchemy_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)


# # Définition du modèle de la table "livres" dans la base de données
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auteur = db.Column(db.String(80), nullable=False)
    titre = db.Column(db.String(80), nullable=False)
    annee = db.Column(db.Integer)


        
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'auteur': self.auteur,
            'annee': self.annee
        }
        


@app.route('/')
def index():
    all_data=Book.query.all()
    return render_template("index.html",Books=all_data)

@app.route('/')
def index():

    return render_template("index.html")



# Définition des routes de l'API REST
@app.route('/Books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [Livre.to_dict() for Livre in books]
    return jsonify(book_list)


@app.route('/api/livres/auteur/<string:auteur>/', methods=["GET"])
def getBooksByAuthor(auteur):
    books = Book.query.filter_by(auteur=auteur).all()
    if books:
        books_list = [book.to_dict() for book in books]
        return jsonify(books_list)
    else:
        return {"error": "Books not found."}


@app.route('/insert', methods=['POST'])
def Insert():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']
        last_book = Book.query.order_by(Book.id.desc()).first()
        

        # Si la table est vide, initialiser i à 0
        if last_book is None:
            i = 0
        else:
            i = last_book.id
        livre = Book(id=i+1,titre=titre, auteur=auteur, annee=annee)
        db.session.add(livre)
        db.session.commit()
        flash('Book inserted successfully')
        return(jsonify(livre.to_dict()))

@app.route('/update',methods=['GET','POST'])
def Update():
    if request.method=='POST':
        my_data=Book.query.get(request.form.get('id'))
        my_data.auteur = request.form['auteur']
        my_data.titre=request.form['titre']
        my_data.annee=request.form['annee']
        
        db.session.commit()
        flash('Book updated successfully')
        return redirect(url_for('index'))
    
@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    my_data=Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book deleted successfully")
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)