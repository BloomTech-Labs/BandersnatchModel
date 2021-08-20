import pandas as pd
import altair as alt
from MonsterLab import Monster


class Data:

    def __init__(self):
        self.path = "app/data_source/monsters.csv"
        self.df = pd.read_csv(self.path)

    def create(self, data):
        self.df = self.df.append(data, ignore_index=True)
        self._update()

    def delete(self, indices):
        self.df = self.df.drop(index=indices)
        self._update()

    def seed(self, n_monsters):
        self.df = pd.concat([
            self.df,
            pd.DataFrame(Monster().to_dict() for _ in range(n_monsters)),
        ])
        self._update()

    def _update(self):
        self.df.to_csv(self.path, index=False)
        self.df = pd.read_csv(self.path)

    def read(self):
        return self.df.drop(columns=[
            "Name", "Damage", "Type", "Time Stamp",
        ])

    @property
    def count(self):
        return self.df.shape[0]

    def visualize(self, x_axis, y_axis, target, rarity):
        text_color = "#AAAAAA"
        graph_color = "#333333"
        graph_bg = "#252525"

        if rarity != "All":
            data = self.df[self.df['Rarity'] == rarity]
        else:
            data = self.df

        graph = alt.Chart(
            data,
            title="Monsters",
        ).mark_circle(size=100).encode(
            x=alt.X(x_axis, axis=alt.Axis(title=x_axis)),
            y=alt.Y(y_axis, axis=alt.Axis(title=y_axis)),
            color=target,
            tooltip=alt.Tooltip(list(self.df.columns)),
        ).properties(
            width=400,
            height=440,
            background=graph_bg,
            padding=40,
        ).configure(
            legend={
                "titleColor": text_color,
                "labelColor": text_color,
                "padding": 10,
            },
            title={
                "color": text_color,
                "fontSize": 26,
                "offset": 30,
            },
            axis={
                "titlePadding": 20,
                "titleColor": text_color,
                "labelPadding": 5,
                "labelColor": text_color,
                "gridColor": graph_color,
                "tickColor": graph_color,
                "tickSize": 10,
            },
            view={
                "stroke": graph_color,
            },
        )
        return graph
