# from kasuhara_web.app import db
# from kasuhara_web.apps.auth_web.forms import LoginForm
# from flask import Blueprint, flash, render_template
from apps.app import db
from apps.auth_web.forms import UserLoginForm, ShopLoginForm
from apps.crud.models import User, Shop
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_user, logout_user
import hashlib
 




# Blueprintを使ってauthを生成する
auth_web = Blueprint(
    "auth_web",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@auth_web.route("/user_login", methods=["GET", "POST"])
def user_login():
    form = UserLoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        
        if user is not None and (user.password_hash == hash_password(form.password.data)):
            # ユーザーの削除フラグがTrueの場合はログインを拒否
            if user.delete_flag:
                flash("このユーザーは削除されているためログインできません。")
                return redirect(url_for("auth_web.user_login"))
            
            session['user_id'] = user.user_id
            session.permanent = True
            if user.user_id == "admin001":
                return redirect(url_for("crud.shop_list"))
            return redirect(url_for("auth_web.shop_login"))
        
        flash("ユーザーIDかパスワードが不正です。")
    
    return render_template("auth_web/LoginWebUser.html", form=form)




@auth_web.route("/shop_login", methods=["GET", "POST"])
def shop_login():
    form = ShopLoginForm()
    if form.validate_on_submit():
        # 店舗IDから店舗を取得する
        shop = Shop.query.filter_by(shop_id=form.shop_id.data).first()
        
        # 店舗が存在し、パスワードが一致する場合
        if shop is not None:
            # 店舗の削除フラグがTrueの場合はログインを拒否
            if shop.delete_flag:
                flash("この店舗は削除されているためログインできません。")
                return redirect(url_for("auth_web.shop_login"))
            
            session['shop_id'] = shop.shop_id
            session.permanent = True
            if shop.shop_id == "admin001" and (shop.admin_password == hash_password(form.password.data)):
                print()
                return redirect(url_for("crud.shop_list"))
            if (shop.admin_password == hash_password(form.password.data)):
                return redirect(url_for("detector.HistoryTop"))
        
        flash("店舗IDかパスワードが不正です。")
    return render_template("auth_web/LoginWebShop.html", form=form)




def hash_password(password):
  hash_object = hashlib.sha256()
  hash_object.update(password.encode('utf-8'))
  return hash_object.hexdigest()