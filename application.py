from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///champions.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Lolfanart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    champion = db.Column(db.String(50), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    like = db.Column(db.Integer, default=0)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('IncLike','None') == 'None':
            search = str(request.form['search'])
            images = []
            obj = db.session.query(Lolfanart).filter_by(nickname=search).order_by(desc(Lolfanart.id)).all()
            print(obj)
            for i in obj:
                image = b64encode(i.image).decode('utf-8')
                images.append(image)
            return render_template('PersonsPage.html', search=search, images=images)
        else:
            user = Lolfanart.query.filter_by(nickname=request.form["search"]).first()
            user.like += 1
            db.session.commit()
    images = {}
    obj = Lolfanart.query.all()
    for i in obj:
        nicksnlikes = (i.nickname, i.like)
        image = b64encode(i.image).decode("utf-8")
        images[image] = nicksnlikes
    return render_template('index.html', images=images.items())

@app.route('/aboutus')
def about():
    return render_template('aboutUs.html')



@app.route('/addpage', methods=['GET', 'POST'])
def yourpage():
    champions = ['Aatrox', 'Annie', 'Ahri', 'Ashe', 'Braum', 'Poppy']
    if request.method == 'POST':
        champion = request.form['ChampionSelect']
        nickname = request.form['Name']
        image = request.files['Image'].read()
        b1 = Lolfanart(nickname=nickname, champion=champions[int(champion)], image=image)
        db.session.add(b1)
        db.session.commit()
        return champions[int(champion)] + ' ' + nickname + 'updated'
    return render_template('addpost.html', champions=champions)


@app.route('/gift')
def gift():
    return render_template('gift.html')



if __name__ == '__main__':
    app.run(debug=True)
