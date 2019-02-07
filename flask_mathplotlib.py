""" Shows how to use flask and matplotlib together.
Shows SVG, and png.
The SVG is easier to style with CSS, and hook JS events to in browser.
python3 -m venv venv
. ./venv/bin/activate
pip install flask matplotlib
python flask_matplotlib.py
"""
import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG

from matplotlib.figure import Figure

app = Flask(__name__)


@app.route("/")
def index():
    """ Returns html with the img tag for your plot.
    """
    num_x_points = int(request.args.get("num_x_points", 5))
    # in a real app you probably want to use a flask template.
    return f"""
    <h1>Flask and matplotlib</h1>
    <h2>Random data with num_x_points={num_x_points}</h2>
    <form method=get action="/">
      <input name="num_x_points" type=number value="{num_x_points}" />
      <input type=submit value="update graph">
    </form>
    <h3>Plot as a png</h3>
    <img src="/matplot-as-image-{num_x_points}.png"
         alt="random points as png"
         height="200"
    >
    <h3>Plot pie chart as a SVG</h3>
    <img src="/matplot-as-image-{num_x_points}.svg"
         alt="random pie chart as svg"
         height="200"
    >
    <h3>Plot polar as a SVG</h3>
    <img src="/polar-as-image-{num_x_points}.svg"
         alt="random polar as svg"
         height="200"
    >
    """



    # from flask import render_template
    # return render_template("yourtemplate.html", num_x_points=num_x_points)


@app.route("/matplot-as-image-<int:num_x_points>.png")
def plot_png(num_x_points=5):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


def plot_svg(num_x_points=5):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


@app.route("/matplot-as-image-<int:parts>.svg")
def plot_pie(parts=5):
    import matplotlib.pyplot as plt
    from utils.rndm import randomword

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = [randomword(6) for i in range(parts)]
    sizes = [random.randint(1,101) for i in range(parts)]#15, 30, 45, 10]
    explode = [0] * parts #(0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    explode[random.randint(0,parts)] = 0.1

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    output = io.BytesIO()
    FigureCanvasSVG(fig1).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")
    #
    # sunalt = df_week_max_angle.plot().get_figure()
    # buf = io.BytesIO()
    # sunalt.savefig(buf, format='png')
    # buf.seek(0)
    #
    # plt.plot()


@app.route("/polar-as-image-<int:parts>.svg")
def polar_pie(parts):
    """
    =======================
    Pie chart on polar axis
    =======================

    Demo of bar plot on a polar axis.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure()
    # Compute pie slices
    N = 20
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    radii = 10 * np.random.rand(N)
    width = np.pi / 4 * np.random.rand(N)

    ax = plt.subplot(111, projection='polar')
    bars = ax.bar(theta, radii, width=width, bottom=0.0)

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.viridis(r / 10.))
        bar.set_alpha(0.5)
    #
    # plt.savefig('foo.png')
    # plt.close()

    fig.savefig('temp.png', dpi=fig.dpi)
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == "__main__":
    import webbrowser
    import os
    #webbrowser.open("http://127.0.0.1:5000/")
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
