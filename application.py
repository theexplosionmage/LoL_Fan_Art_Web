from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
from sqlalchemy import desc

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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        images = []
        obj = Posts.query.order_by(desc(Posts.id)).all()
        for i in obj:
            image = b64encode(i.image).decode("utf-8")
            images.append(image)
        return render_template('index.html', images=images)
    if request.method == 'POST':
        search = str(request.form['search'])
        images = []
        obj = db.session.query(Posts).filter_by(Nickname=search).order_by("id desc").all()
        print(obj)
        for i in obj:
            image = b64encode(i.image).decode('utf-8')
            images.append(image)
        return render_template('PersonsPage.html', search=search, images=images)


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
        b1 = Posts(Nickname=nickname, champion=champions[int(champion)], image=image)
        db.session.add(b1)
        db.session.commit()
        return champions[int(champion)] + ' ' + nickname + 'updated'
    return render_template('addpost.html', champions=champions)


@app.route('/gift')
def gift():
    return render_template('gift.html')

if __name__ == '__main__':
    app.run(debug=True)
