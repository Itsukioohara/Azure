from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


# db.Modelを継承したUserクラスを作成する
class User(db.Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = "USERS"
    # カラムを定義する
    user_id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String, index=True)
    delete_flag = db.Column(db.Boolean)


    # パスワードチェックをする
    def verify_password(self, password):
        return (self.password_hash==password)


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Shopクラスを作成
class Shop(db.Model, UserMixin):
    # テーブル名
    __tablename__ = "SHOP"
    # カラムを定義します
    shop_id = db.Column(db.String, primary_key=True)
    counter_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    address = db.Column(db.String)
    tel = db.Column(db.String)
    general_password = db.Column(db.String)
    delete_flag = db.Column(db.Boolean)
    admin_password = db.Column(db.String)
    
    
# ログインしている店舗情報を取得する関数を作成する
@login_manager.user_loader
def load_shop(shop_ai):
    return Shop.query.get(shop_ai)