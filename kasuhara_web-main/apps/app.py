# Flaskクラスをimportする
from flask import Flask,url_for,redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_session import Session

# from apps.crud.views import crud
from apps.config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth_web.login_web_user"
login_manager.login_message = ""

def create_app(config_key):
    print("----------------------------------------")
    app = Flask(__name__)
    app.config.from_object(config[config_key])
   # アプリのコンフィグ設定をする
    app.config.from_mapping(
       SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
       SESSION_TYPE='filesystem',
       SQLALCHEMY_DATABASE_URI=
       'mssql+pyodbc://kasuhara-itsuki:' + '2brJmrCN3SfN' +
       '@kasuhara-sql-server.database.windows.net:1433/kasuhara_database2?driver=ODBC+Driver+18+for+SQL+Server',
       SQLALCHEMY_TRACK_MODIFICATIONS=False,
       SQLALCHEMY_ECHO=True,
   )
   # SQLAlchemyとアプリを連携する
    db.init_app(app)
   # Migrateとアプリを連携する
    Migrate(app, db)
   #login_magagerをアプリケーションと連携する
    login_manager.init_app(app)
 
    
    # これから作成するauthパッケージからviewsをimportする
    from apps.auth_web import views as auth_web_views
    
    from apps.detector import views as detector_views
    
    from apps.crud import views as crud_views
    
    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_web_views.auth_web, url_prefix="/auth")
    app.register_blueprint(detector_views.dt, url_prefix="/detector")
    app.register_blueprint(crud_views.crud, url_prefix='/crud')
    
    @app.route("/")
    def index():
        return redirect(url_for(".auth_web.shop_login"))
    
    return app

# URLと実行する関数をマッピングする
