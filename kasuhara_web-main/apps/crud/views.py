from apps.app import db
from apps.crud.forms import UserForm
from apps.crud.models import User
from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
import hashlib

from flask import Blueprint, render_template, request, redirect, url_for
from .models import Shop, User
from apps.app import db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Blueprintでcrudアプリを生成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# indexエンドポイントを作成しindex.htmlを返す
@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください"


@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserFormをインスタンス化する
    form = UserForm()

    # フォームの値をバリデートする
    if form.validate_on_submit():
        # ユーザーを作成する
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # ユーザーを追加してコミットする
        db.session.add(user)
        db.session.commit()

        # ユーザーの一覧画面へリダイレクトする
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
@login_required
def users():
    """ユーザーの一覧を取得する"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)




# methodsにGETとPOSTを指定する
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    # Userモデルを利用してユーザーを取得する
    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザーを更新しユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GETの場合はHTMLを返す
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))




@crud.route('/shop_list', methods=['GET'])
def shop_list():
    query = request.args.get('query')
    filter = request.args.get('filter', 'name')  # デフォルトは店舗名で検索

    if query:
        # 部分一致検索
        if filter == 'name':
            shops = Shop.query.filter(Shop.name.like(f"%{query}%")).all()
        elif filter == 'address':
            shops = Shop.query.filter(Shop.address.like(f"%{query}%")).all()
        elif filter == 'tel':
            shops = Shop.query.filter(Shop.tel.like(f"%{query}%")).all()
    else:
        shops = Shop.query.all()  # クエリが空の場合は全件取得

    return render_template('crud/ShopList.html', shops=shops)




@crud.route('/shop/<shop_id>/edit', methods=['GET', 'POST'])
def edit_shop(shop_id):
    shop = Shop.query.filter_by(shop_id=shop_id).first_or_404()

    if request.method == 'POST':
        # 店舗情報の更新
        shop.name = request.form['name']
        shop.address = request.form['address']
        shop.tel = request.form['tel']
        shop.delete_flag = 'delete_flag' in request.form  # チェックボックス処理
        db.session.commit()

        return redirect(url_for('crud.shop_list', shop_id=shop_id))

    return render_template('crud/EditShop.html', shop=shop)



@crud.route('/user', methods=['GET'])
def user_list():
    query = request.args.get('query', '')  # 検索クエリ
    users = User.query.filter(User.user_id.like(f'%{query}%')).order_by(User.user_id).all()
    return render_template('crud/UserList.html', users=users, query=query)



@crud.route('/user/<user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.filter_by(user_id=user_id).first_or_404()

    if request.method == 'POST':
        user.password_hash = hash_password(request.form['password']) if request.form['password'] else user.password_hash
        user.delete_flag = 'delete_flag' in request.form  # チェックボックス処理
        db.session.commit()
        return redirect(url_for('crud.user_list'))

    return render_template('crud/EditUser.html', user=user)




@crud.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # パスワードのハッシュ化
        password_hash = hash_password(password)

        # 新しいユーザーのインスタンスを作成
        new_user = User(
            user_id=user_id,
            password_hash=password_hash,
            delete_flag=False  # 削除フラグはFalse
        )

        # セッションに追加し、データベースにコミット
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('crud.user_list'))  # ユーザー一覧ページへリダイレクト

    return render_template('crud/AddUser.html')  # ユーザー追加ページ











@crud.route('/add_shop', methods=['GET', 'POST'])
def add_shop():
    if request.method == 'POST':
        shop_id = request.form['shop_id']
        name = request.form['name']
        address = request.form['address']
        tel = request.form['tel']
        general_password = request.form['general_password']
        admin_password = request.form['admin_password']
        counter_number = request.form['counter_number']  # カウンター番号の取得
        

        # パスワードのハッシュ化
        general_password = hash_password(general_password)
        admin_password = hash_password(admin_password)
        

        # 新しい店舗のインスタンスを作成
        new_shop = Shop(
            shop_id=shop_id,
            name=name,
            address=address,
            tel=tel,
            general_password=general_password,
            admin_password=admin_password,
            delete_flag=False,  # 削除フラグはFalse
            counter_number=counter_number  # カウンター番号を設定
        )

        # セッションに追加し、データベースにコミット
        db.session.add(new_shop)
        db.session.commit()
        return redirect(url_for('crud.shop_list'))  # 店舗一覧ページへリダイレクト

    return render_template('crud/AddShop.html')
















def hash_password(password):
  hash_object = hashlib.sha256()
  hash_object.update(password.encode('utf-8'))
  return hash_object.hexdigest()