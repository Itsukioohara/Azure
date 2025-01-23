from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class UserLoginForm(FlaskForm):
    user_id = StringField(
        "ユーザーID",
        validators=[
            DataRequired("ユーザーIDは必須です。"),
        ],
    )
    
    password = PasswordField("Password", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("ログイン")
    
    
class ShopLoginForm(FlaskForm):
    shop_id = StringField(
        "店舗ID",
        validators=[
            DataRequired("店舗IDは必須です。"),
        ],
    )
    
    password = PasswordField("Password", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("ログイン")