from flask import Blueprint, render_template, url_for, request, session, redirect
from couple_ways.forms import NewTripForm


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@pages.route("/")
def landing_page():
    return render_template(
        "landing_page.html",
        title="Couple Ways",
    )

@pages.route("/toogle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else: 
        session["theme"] = "dark"
        
    return redirect(request.args.get("current_page"))

@pages.route("/add_trip", methods=["GET", "POST"])
def add_trip():
    form= NewTripForm()
    
    if request.method == "POST":
        pass
    
    return render_template("add_trip.html", title="Couple Ways - Add Trip", form=form)

@pages.route("/my_trips")
def my_trips():
    return render_template(
        "my_trips.html",
        title="Couple Ways - Trips",
    )