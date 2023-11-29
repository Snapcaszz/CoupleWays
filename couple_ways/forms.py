from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import InputRequired, NumberRange, DataRequired, ValidationError
from couple_ways.utils.functions import youtube_url_to_embed


class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        # checks valuelist contains at least 1 element, and the first element isn't falsy (i.e. empty string)
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []


class NewTripForm(FlaskForm):
    destination = StringField("Where do you want to go?", validators=[InputRequired()])
    start_date = DateField(
        "When does your trip start?", format='%Y-%m-%d', validators=[DataRequired()]
    )
    end_date = DateField(
        "When do you come back?", format='%Y-%m-%d', validators=[DataRequired()]
    )
    current_budget = FloatField(
        "What is your current budget?",
        render_kw={"placeholder": "Enter a positive number!"},
        validators=[
            InputRequired(message='Please enter valid budget'),
            NumberRange(min=0, max=None, message='Please enter a positive number!'),
        ],
    )
    travelers = StringListField(
        "Who will go on this trip?",
        render_kw={"placeholder": "Enter one name each line"},
        validators=[InputRequired()],
    )
    submit = SubmitField("Create my Trip")
    
    def validate_end_date(form, field):
        if form.start_date.data and field.data:
            if form.start_date.data >= field.data:
                raise ValidationError("End date must be higher than the start date.")

class EditTripForm(NewTripForm):
    destination = StringField("Trip Destination:", validators=[InputRequired()])
    current_budget = FloatField(
        "What is your current budget?",
        render_kw={"placeholder": "Enter a positive number!"},
        validators=[
            InputRequired(message='Please enter valid budget'),
            NumberRange(min=0, max=None, message='Please enter a positive number!'),
        ],
    )
    trip_itinerary = StringListField("Describe the itinerary for this trip!")
    video_of_the_trip = StringField(
        "Youtube Video for this trip:",
        render_kw={"placeholder": "https://youtu.be/WMkg42p4FMU?si=9fuHY0fzfu4FlXhs"},
        )
    submit = SubmitField("Edit Trip")
    
    def validate_video_of_the_trip(form, field):
        if field.data:
            video_embed= youtube_url_to_embed(field.data)
            if not video_embed: 
                raise ValidationError("Input the right link format!")