from flask import Flask, jsonify, request
import csv
from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from contentbased_filtering import getRecommendations

all_articles = []

with open('articles.csv', encoding = "utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
not_liked_articles = []

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_articles.append(article)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    popular_article_data = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        popular_article_data.append(_d)
    return jsonify({
        "data": popular_article_data,
        "status": "success"
    }), 201

@app.route("/recommended-articles")
def recommended_articles():
    r_article_data = []
    for recommended in getRecommendations():
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        r_article_data.append(_d)
    return jsonify({
        "data" : r_article_data,
        "status" : "success!"
    }),200

if __name__ == "__main__":
  app.run()