from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import InputRequired, NumberRange, DataRequired


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
        "When does your trip start?", format="%d-%m-%Y", validators=[DataRequired()]
    )
    end_date = DateField(
        "When do you come back?", format="%d-%m-%Y", validators=[DataRequired()]
    )
    current_budget = StringField(
        "What is your current budget?",
        render_kw={"placeholder": "Enter a number!"},
        validators=[
            InputRequired()
        ],
    )
    travelers = StringListField(
        "Who will go on this trip?",
        render_kw={"placeholder": "Enter one name each line"},
        validators=[InputRequired()],
    )
    submit = SubmitField("Create my Trip")
