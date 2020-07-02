from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///champions.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nickname = db.Column(db.String(100), nullable=False)
    champion = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)


b1 = Posts.query.all()
print(b1[0].Nickname)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addpage', methods=['GET', 'POST'])
def yourpage():
    champions = ['Aatrox', 'Annie', 'Ahri', 'Ashe', 'Braum']
    if request.method == 'POST':
        champion = request.form['ChampionSelect']
        nickname = request.form['Name']
        image = request.files['Image'].read()
        b1 = Posts(Nickname=nickname, champion=champions[int(champion)], image=image)
        db.session.add(b1)
        db.session.commit()
        return champions[int(champion)] + ' ' + nickname + 'updated'
    return render_template('addpost.html', champions=champions)


if __name__ == '__main__':
    app.run(debug=True)
