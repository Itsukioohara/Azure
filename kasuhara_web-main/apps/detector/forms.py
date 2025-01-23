from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField





class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
