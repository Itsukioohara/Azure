from apps.app import db
from apps.crud.models import Shop
from apps.detector.models import MovieList
from flask import Blueprint

from apps.crud.models import Shop

# UploadImageFormをimportする
from apps.detector.models import MovieList
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
    flash,
    request,
)

# template_folderを指定する（staticは指定しない）
dt = Blueprint("detector", __name__, template_folder="templates")


@dt.route("/history_top", methods=["GET", "POST"])
def HistoryTop():
    # SHOPとMOVIEをJoinして動画履歴を取得する
    movie_list = (
        db.session.query(Shop, MovieList)
        .join(MovieList, (Shop.shop_id == MovieList.shop_id) & (Shop.counter_number == MovieList.counter_number))
        .all()
    )
    
    return render_template("detector/HistoryTop.html", movie_list=movie_list)


# 履歴検索
@dt.route("/images/search", methods=["GET"])
def search():
    # GETパラメータから検索ワードを取得する
    search_text = request.args.get("search")
    
    # 検索条件に基づいてMOVIEを取得する
    if search_text:
        filtered_movie_list = (
            db.session.query(Shop, MovieList)
            .join(MovieList, (Shop.shop_id == MovieList.shop_id) & (Shop.counter_number == MovieList.counter_number))
            .filter(
                (MovieList.movie_id.like(f"%{search_text}%")) | 
                (MovieList.movie_pass.like(f"%{search_text}%"))
            )
            .all()
        )
    else:
        # 検索条件がない場合は全件取得
        filtered_movie_list = (
            db.session.query(Shop, MovieList)
            .join(MovieList, (Shop.shop_id == MovieList.shop_id) & (Shop.counter_number == MovieList.counter_number))
            .all()
        )
    
    return render_template(
        "detector/HistoryTop.html",
        movie_list=filtered_movie_list,
    )
    
from flask import render_template
from apps.detector.models import MovieList

# 動画詳細ページ
@dt.route("/view_movie/<movie_id>")
def view_movie(movie_id):
    # movie_id を基に MovieList から動画情報を取得
    movie = MovieList.query.filter_by(movie_id=movie_id).first_or_404()
    
    return render_template('detector/MovieView.html', movie=movie)
