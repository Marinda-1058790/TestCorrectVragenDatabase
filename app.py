import os.path
import sys
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, session

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database
from lib.vragenmodel import VragenModel

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, "databases", "testcorrect_vragen.db")
app.secret_key = 'ThisKeyIsSuperSecret'

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)


vragen_model = VragenModel(DATABASE_FILE)
# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.before_request
def check_login():
    if request.endpoint not in ["static", "loginpage", "login"]:
        if not session.get("logged_in"):
            return redirect(url_for("loginpage"))


@app.route("/")
def loginpage():
    return render_template("loginpage.html")


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


@app.route("/leerdoelen")
def leerdoelen():
    vragen = vragen_model.get_vragen_without_leerdoel()
    leerdoelen = vragen_model.get_leerdoel()
    return render_template("leerdoelen.html", vragen=vragen, leerdoelen=leerdoelen)


@app.route("/leerdoel_opslaan/<vraag_id>", methods=["POST"])
def leerdoel_opslaan(vraag_id):
    if request.form["leerdoel"] == 0:
        return redirect(url_for("leerdoelen"))
    else:
        vragen_model.save_leerdoel(vraag_id, request.form["leerdoel"])
        return redirect(url_for("leerdoelen"))


@app.route("/uitzondering_leerdoel/<vraag_id>", methods=["POST"])
def uitzondering_leerdoel(vraag_id):
    vragen_model.exception_leerdoel(vraag_id)
    return redirect(url_for("leerdoelen"))


@app.route("/auteurs")
def auteurs():
    vragen = vragen_model.get_vragen_without_auteur()
    auteurs = vragen_model.get_auteur()
    return render_template("auteurs.html", vragen=vragen, auteurs=auteurs)


@app.route("/auteur_opslaan/<vraag_id>", methods=["POST"])
def auteur_opslaan(vraag_id):
    if request.form["auteur"] == 0:
        return redirect(url_for("auteurs"))
    else:
        vragen_model.save_auteur(vraag_id, request.form["auteur"])
        return redirect(url_for("auteurs"))


@app.route("/auteurs_select")
def auteurs_select():
    vragen = vragen_model.get_vragen_with_auteur()
    auteurs = vragen_model.get_auteur()
    return render_template("auteurs_select.html", vragen=vragen, auteurs=auteurs)


@app.route("/auteurs_selectresults", methods=["POST"])
def auteurs_selectresults():
    selected_auteurs = request.form.getlist("auteurs")
    vragen = vragen_model.get_vragen_of_selected_auteurs(selected_auteurs)
    auteurs = vragen_model.get_auteur()
    return render_template("auteurs_select.html", vragen=vragen, auteurs=auteurs)


@app.route("/htmlcodes")
def htmlcodes():
    foutcodes = vragen_model.get_vragen_with_htmlcodes()
    return render_template("htmlcodes.html", foutcodes=foutcodes)


@app.route("/vraag_opslaan/<vraag_id>", methods=["POST"])
def vraag_opslaan(vraag_id):
    print("test")
    print(request.form["vraag"])
    vragen_model.save_vraag(vraag_id, request.form["vraag"])
    return redirect(url_for("htmlcodes"))


@app.route("/database")
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["logged_in"] = False

    authenticated = (username == "test_username", password == "test_password")

    if authenticated:
        session["logged_in"] = True
        return redirect(url_for("homepage"))

    else:
        flash("invalid login credentials")
        return redirect(url_for("loginpage"))


@app.route("/auteursdata")
def auteursdata():
    medewerker = vragen_model.get_incorrect_medewerkers()
    return render_template("auteursdata.html", auteurs=medewerker)


@app.route("/medewerker_opslaan/<auteur_id>", methods=["POST"])
def medewerker_opslaan(auteur_id):
    vragen_model.save_medewerker(auteur_id, request.form["medewerker"])
    return redirect(url_for("auteursdata"))


@app.route("/uitzondering")
def uitzondering():
    uitzondering = vragen_model.get_uitzondering()
    leerdoelen = vragen_model.get_leerdoel_column()
    auteurs = vragen_model.get_auteur_column()
    return render_template(
        "uitzondering.html",
        uitzondering=uitzondering,
        leerdoelen=leerdoelen,
        auteurs=auteurs,
    )


@app.route("/uitzondering_terugzetten/<vraag_id>", methods=["POST"])
def uitzondering_terugzetten(vraag_id):
    vragen_model.uitzondering_terugzetten(vraag_id)
    return redirect(url_for("uitzondering"))


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
