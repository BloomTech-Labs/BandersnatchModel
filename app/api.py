import random

from MonsterLab import Monster
from flask import Flask, render_template, request

from app.data import Data
from app.model import Model

API = Flask(__name__)
API.data = Data()
API.model = Model(API.data)


@API.route("/")
def home():
    return render_template("index.html")


@API.route("/create", methods=["GET", "POST"])
def create():
    name = request.values.get("name")
    monster_type = request.values.get("type") or "Dragon"
    level = int(request.values.get("level") or 1)
    rarity = request.values.get("rarity") or "Rank 0"

    if name:
        monster = Monster(name, monster_type, level, rarity)
        API.data.create(monster.to_dict())
        monster_data = monster.to_dict()
    else:
        monster_data = None

    return render_template(
        "create.html",
        name=name,
        monster_type=monster_type,
        level=level,
        rarity=rarity,
        monster=monster_data,
    )


@API.route("/data")
def data():
    df_table = API.data.df.to_html()
    return render_template(
        "data.html",
        df_table=df_table,
    )


@API.route("/view", methods=["GET", "POST"])
def view():
    x_axis = request.values.get("x_axis", "Health")
    y_axis = request.values.get("y_axis", "Energy")
    target = request.values.get("target", "Rarity")
    rarity = request.values.get("rarity", "All")
    graph = API.data.visualize(x_axis, y_axis, target, rarity)
    return render_template(
        "view.html",
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        rarity=rarity,
        graph_json=graph.to_json(),
    )


@API.route("/train")
def train():
    return render_template(
        "train.html",
        name=API.model.name,
        time_stamp=API.model.time_stamp,
        test_score=API.model.score(),
        total=API.model.total,
        available=API.data.count - API.model.total,
    )


@API.route("/predict", methods=["GET", "POST"])
def predict():
    level = int(request.values.get("level", random.randint(1, 20)))
    health = float(request.values.get("health", random.gauss(75, 25)))
    energy = float(request.values.get("energy", random.gauss(75, 25)))
    sanity = float(request.values.get("sanity", random.gauss(75, 25)))

    if "submit" in request.values.keys():
        prediction, confidence = API.model([
            level,
            health,
            energy,
            sanity,
        ])
        confidence = f"{100*confidence:.0f}%"
    else:
        prediction, confidence = "", ""

    return render_template(
        "predict.html",
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=confidence,
    )


if __name__ == '__main__':
    API.run()
