import uuid
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from couple_ways.utils.functions import months_between_dates
from math import floor
from flask import jsonify

from flask import (
    Blueprint,
    render_template,
    url_for,
    request,
    session,
    redirect,
    current_app,
    flash,
)
from couple_ways.models import Trip
from couple_ways.forms import NewTripForm, EditTripForm, HotelSimulationForm, TripDeletionForm
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
    form = NewTripForm()

    if form.validate_on_submit():
        trip = Trip(
            _id=uuid.uuid4().hex,
            destination=form.destination.data,
            start_date=datetime.combine(form.start_date.data, time(0, 0, 0)),
            end_date=datetime.combine(form.end_date.data, time(0, 0, 0)),
            current_budget=form.current_budget.data,
            travelers=form.travelers.data,
        )

        current_app.db.trips.insert_one(asdict(trip))
        return redirect(url_for(".my_trips"))

    return render_template("add_trip.html", title="Couple Ways - Add Trip", form=form)


@pages.route("/my_trips")
def my_trips():
    trip_data = current_app.db.trips.find({})
    trips = [Trip(**trip) for trip in trip_data]
    for trip in trips:
        trip.start_date = trip.start_date.date().strftime("%d %b %Y")
        trip.end_date = trip.end_date.date().strftime("%d %b %Y")

    return render_template(
        "my_trips.html", title="Couple Ways - Trips", trips_data=trips
    )


@pages.get("/trip/<string:_id>/rate")
def rate_trip(_id):
    rating = int(request.args.get("rating"))
    try:
        result = current_app.db.trips.update_one(
            {"_id": _id}, {"$set": {"rating": rating}}
        )
        print(
            f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)."
        )
    except Exception as e:
        print(f"Error: {e}")

    return redirect(url_for(".my_trips"))


@pages.get("/trip/<string:_id>/rate/this")
def rate_this_trip(_id):
    rating = int(request.args.get("rating"))
    try:
        result = current_app.db.trips.update_one(
            {"_id": _id}, {"$set": {"rating": rating}}
        )
        print(
            f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s)."
        )
    except Exception as e:
        print(f"Error: {e}")

    return redirect(url_for(".trip", _id=_id))


@pages.route("/trip/<string:_id>")
def trip(_id: str):
    trip = Trip(**current_app.db.trips.find_one({"_id": _id}))
    trip.calculate_fields

    # creating the labels and values to plot in the trip simulation, I know its confusing and not readable
    # for the labels its ploting each month after the date_to_start_saving until the start_date of the trip, hence the sum of the relative delta of i months
    # the range(floor(months_between_dates(trip.date_to_start_saving, trip.start_date))) iterates the number of months between the two dates, rounded down
    # for the values its ploting the current value added by the amount to save each month after the date to start saving
    if trip.date_to_start_saving:
        labels = [
            (trip.date_to_start_saving + relativedelta(months=i))
            .date()
            .strftime("%d %b %Y")
            for i in range(
                floor(months_between_dates(trip.date_to_start_saving, trip.start_date))
            )
        ]
        values = [
            (trip.current_budget + (i * trip.amount_to_save))
            for i in range(
                floor(months_between_dates(trip.date_to_start_saving, trip.start_date))
            )
        ]
        values_per_people = [
            (trip.current_budget + (i * trip.amount_to_save_per_people))
            for i in range(
                floor(months_between_dates(trip.date_to_start_saving, trip.start_date))
            )
        ]
        
        months_to_save = floor(months_between_dates(trip.date_to_start_saving, trip.start_date))
        
        trip.start_date = trip.start_date.date().strftime("%d %b %Y")
        trip.end_date = trip.end_date.date().strftime("%d %b %Y")

        return render_template(
            "trip.html",
            trip=trip,
            title=f"Couple Ways - {trip.destination}",
            labels=labels,
            values=values,
            values_per_people=values_per_people,
            months_to_save=months_to_save,
        )
    
    trip.start_date = trip.start_date.date().strftime("%d %b %Y")
    trip.end_date = trip.end_date.date().strftime("%d %b %Y")

    return render_template(
        "trip.html",
        trip=trip,
        title=f"Couple Ways - {trip.destination}",
    )


@pages.route("/edit_trip/<string:_id>", methods=["GET", "POST"])
def edit_trip(_id):
    trip = Trip(**current_app.db.trips.find_one({"_id": _id}))
    form = EditTripForm(obj=trip)

    if form.validate_on_submit():
        trip.destination = form.destination.data
        trip.start_date = datetime.combine(form.start_date.data, time(0, 0, 0))
        trip.end_date = datetime.combine(form.end_date.data, time(0, 0, 0))
        trip.current_budget = form.current_budget.data
        trip.travelers = form.travelers.data
        trip.trip_itinerary = form.trip_itinerary.data
        trip.video_of_the_trip = form.video_of_the_trip.data

        trip.get_embed()
        trip.calculate_fields()

        current_app.db.trips.update_one({"_id": trip._id}, {"$set": asdict(trip)})
        return redirect(url_for(".trip", _id=trip._id))

    return render_template("edit_trip.html", title="Couple Ways - Edit Trip", form=form)


@pages.route("/simulate_trip/<string:_id>", methods=["GET", "POST"])
def simulate_trip(_id):
    trip = Trip(**current_app.db.trips.find_one({"_id": _id}))
    form = HotelSimulationForm()

    if form.validate_on_submit():
        trip.hotel = form.hotel.data
        trip.hotel_description = form.hotel_description.data
        trip.hotel_link = form.hotel_link.data
        trip.cost_of_stay = form.cost_of_stay.data
        trip.transportation_cost = form.transportation_cost.data
        trip.amount_to_spend = form.amount_to_spend.data
        trip.date_to_start_saving = datetime.combine(date.today(), time(0, 0, 0))

        trip.calculate_fields()

        current_app.db.trips.update_one({"_id": trip._id}, {"$set": asdict(trip)})
        return redirect(url_for(".trip", _id=trip._id))

    return render_template(
        "simulate_trip.html",
        title="Couple Ways - Hotel Simulation",
        form=form,
        trip=trip,
    )


@pages.route("/delete/trip/<string:_id>", methods=["GET", "POST"])
def delete_trip(_id):
    trip = Trip(**current_app.db.trips.find_one({"_id": _id}))
    form = TripDeletionForm()
    
    if form.validate_on_submit():
        try:
            result = current_app.db.trips.delete_one({"_id": _id})
            if result.deleted_count == 1:
                flash("Trip deleted successfully", "success")
            else:
                flash("Trip not found", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for(".my_trips"))

    return render_template("delete_trip_confirmation.html", form=form, trip=trip, title="Couple Ways - Delete Trip")