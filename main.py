from flask import Flask, render_template, redirect, url_for
# bootstrap libraries
from flask_bootstrap import Bootstrap5
# db libraries
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
# form libraries
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, BooleanField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DATABASE
# initial configuration
class Base(DeclarativeBase):
    pass


# initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


# Form configuration
class CreatePostForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Google address", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets?")
    has_toilet = BooleanField("Has Toilet?")
    has_wifi = BooleanField("Has Toilet?")
    can_take_calls = BooleanField("Can Take Calls?")
    seats = StringField("Approximated seats", validators=[DataRequired()])
    coffee_price = StringField("Approximated price in £", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# index.html action
@app.route('/')
def get_all_coffees():
    result = db.session.execute(db.select(Cafe))
    coffees = result.scalars().all()
    return render_template("index.html", all_coffees=coffees)


# cafe.html action
@app.route('/show_cafe/<int:cafe_id>')
def show_cafe(cafe_id):
    requested_post = db.get_or_404(Cafe, cafe_id)
    return render_template("cafe.html", cafe=requested_post)


# edit cafe action
@app.route("/edit-cafe/<cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    edit_form = CreatePostForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.has_sockets = edit_form.has_sockets.data
        cafe.has_toilet = edit_form.has_toilet.data
        cafe.has_wifi = edit_form.has_wifi.data
        cafe.can_take_calls = edit_form.can_take_calls.data
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id=cafe.id))
    return render_template("make-cafe.html", form=edit_form, is_edit=True)


# add button action
@app.route("/new-cafe", methods=["GET", "POST"])
def add_new_cafe():
    cafe = CreatePostForm()
    if cafe.validate_on_submit():
        new_cafe = Cafe(
            name=cafe.name.data,
            map_url=cafe.map_url.data,
            img_url=cafe.img_url.data,
            location=cafe.location.data,
            has_sockets=cafe.has_sockets.data,
            has_toilet=cafe.has_toilet.data,
            has_wifi=cafe.has_wifi.data,
            can_take_calls=cafe.can_take_calls.data,
            seats=cafe.seats.data,
            coffee_price=cafe.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("get_all_coffees"))
    return render_template("make-cafe.html", form=cafe)


# delete action
@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_coffees"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
