from datetime import datetime
from apps.app import db

class MovieList(db.Model):
    __tablename__ = "MOVIE"
    # shop_idはshopテーブルのidカラムを外部キーとして設定する
    movie_id = db.Column(db.String, primary_key=True)
    shop_id = db.Column(db.String, db.ForeignKey("SHOP.shop_id"))
    counter_number = db.Column(db.Integer)
    kasuhara_day = db.Column(db.DateTime, default=datetime.now)
    warning_level = db.Column(db.Integer)
    movie_pass = db.Column(db.String)