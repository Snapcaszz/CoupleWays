from flask import Blueprint, render_template, url_for, request, session, redirect


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