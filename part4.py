# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

labels = []
values = []
with open('noun_data.csv', 'r') as f:
    data = f.readlines()
    for line in data[1:]:
        a,b = line.split(',')
        b = int(b)
        labels.append(a)
        values.append(b)

# ® https://plot.ly/python/bar-charts/, https://plot.ly/python/static-image-export/
data = [go.Bar(x=labels, y=values)]
layout = go.Layout(title='Noun Data', width=800, height=640)
fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, filename='part4_viz_image.png')