import uuid

from flask import Blueprint, render_template, url_for, request, session, redirect, current_app
from couple_ways.models import Trip
from couple_ways.forms import NewTripForm
from dataclasses import asdict


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
    
    if form.validate_on_submit():
        trip = Trip(
            _id=uuid.uuid4().hex,
            destination=form.destination.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            current_budget=form.current_budget.data,
            travelers=form.travelers.data
        )
        
        current_app.db.trips.insert_one(trip.to_dict())
        return redirect(url_for(".my_trips"))
    
    return render_template("add_trip.html", title="Couple Ways - Add Trip", form=form)

@pages.route("/my_trips")
def my_trips():
    trip_data = current_app.db.trips.find({})
    trips = [Trip(**trip) for trip in trip_data]
    for trip in trips: 
        trip.start_date = trip.start_date.date().strftime('%d %b %Y')
        trip.end_date = trip.end_date.date().strftime('%d %b %Y')
        
    return render_template(
        "my_trips.html",
        title="Couple Ways - Trips", trips_data=trips
    )
    
@pages.get("/trip/<string:_id>/rate")
def rate_trip(_id):
    rating = int(request.args.get("rating"))
    try:
        result = current_app.db.trips.update_one({"_id": _id}, {"$set": {"rating": rating}})
        print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).")
    except Exception as e:
        print(f"Error: {e}")

    return redirect(url_for(".my_trips"))

@pages.get("/trip/<string:_id>/rate/this")
def rate_this_trip(_id):
    rating = int(request.args.get("rating"))
    try:
        result = current_app.db.trips.update_one({"_id": _id}, {"$set": {"rating": rating}})
        print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).")
    except Exception as e:
        print(f"Error: {e}")

    return redirect(url_for(".trip", _id=_id))

@pages.route("/trip/<string:_id>")
def trip(_id: str):
    trip = Trip(**current_app.db.trips.find_one({"_id": _id}))
    trip.recalculate_fields
    trip.start_date = trip.start_date.date().strftime('%d %b %Y')
    trip.end_date = trip.end_date.date().strftime('%d %b %Y')
    
    return render_template("trip.html", trip=trip)