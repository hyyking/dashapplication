'''
Main page includes:
>Navbar
>Checkboxes to add elements to the graph
>Main Graph
>Subplot
'''

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
from .app import app
import http.client as httplib
from .modules.config import Config

from plotly import tools
import plotly.graph_objs as go

from .modules.webrequest import WebRequest
from .modules.dataframeoperations import dfOperations


'''Copy of the MaterializeCSS Navbar but adjusted elements
Only one callback for the internet status
'''
header=html.Nav(children=[
	html.Div(className='teal nav-wrapper', children=[
		html.A(href='#', className='brand-logo right', children='Application'),
		html.Ul(id='nav-mobile', className='left hide-on-med-and-down', children=[
			html.Li(children=[html.A(href='/graphs', children='Graphs')]),
			html.Li(children=[html.A(href='/projet', children='Project')]),
			html.Li(children=[html.A(id='internet-status-graphs', href='/internet', children='Status')])
		])
	]),
])


'''Content of the page
Three callbacks:
>Checkboxes
>Main graph
>Subplot
'''
content=html.Div(style={'padding':'0px 10px 15px 10px'}, children=[	
	html.Form(action='#', className='center-align', children=[
		html.Table(children=[
			html.Tr(children=[
				html.Td(style={'padding-right':'0', 'margin':'0', 'width':'200px'}, children=[
					html.P(children=[
						html.Label(className="checkbox-inline", children=[
							dcc.Input(type="checkbox", id='movave'),
							html.Span(children=['Moving Average'])
						])
					])
				]),
				html.Td(style={'padding-left':'0', 'margin':'0'}, children=[
					html.P(children=[
						html.Label(className="checkbox-inline", children=[
							dcc.Input(type="checkbox"),
							html.Span(children=['###'])
						])
					])
				]),
			])
		])
		
	]),

	dcc.Graph(id='main-graph', animate=True),
	dcc.Graph(id='standartdev-graph', animate=False),
	html.P(id='test')
])

'''Intervals and placeholders
One callback to update the current information held in the placeholder div'''
updates=html.Div(children=[
	dcc.Interval(id='internet-update', interval= Config.internet_status_update*1000),
	dcc.Interval(id='graph-update', interval= Config.graph_update*1000, n_intervals=0),
	html.Div(id='placeholder')
])

'''Compacted layout for usage in main.py
Also contains the styling of the layout of the app'''
LAYOUT = html.Div(style={'backgroundColor':'#FFFFFF','marginLeft':'auto','marginRight':'auto',"width":"70%",'boxShadow':'0px 0px 5px 5px rgba(204,204,204,0.4)'}, children=[header, content, updates])

'''Information for the component update'''
kraken = 'https://www.kraken.com/charts'
div = ['div', {'class':'val mono', 'name':'last'}, 'value']
span = ['span', {'class':'pairtext'}, 'tag']
data = dfOperations('final.csv')
data.index_time()

'''Callback for the placeholder, every [Config.graph_update]'''
@app.callback(Output('placeholder','children'), [Input('graph-update', 'n_intervals')])
def updateplaceholder(interval):
	request = WebRequest(kraken, [div,span])
	price, name, time = request.csv_request('final.csv')
	data.add_data({'Price':[price],'Tag':[name],'Time':[time]})
	return '{}|{}|{}'.format(price, name, time)


'''Callback for the main graph updates when the placeholder is updated'''
@app.callback(Output('main-graph', 'figure'), [Input('placeholder', 'children')])
def gen_main_graph(child):
	'''First trace'''
	trace = go.Scatter(
		y=data.data.tail(n=10).Price,
		x=data.data.tail(n=10).index,
		line=go.Line(
			color='#009688'
		),
		hoverinfo='XBT/EUR',
		mode='lines+markers'
	)
	'''styking of the graph element'''
	layout = go.Layout(
		height=450,
		xaxis=dict(
			range = [data.data.tail(n=10).index.min(),data.data.tail(n=10).index.max()],
			showgrid=True,
			showline=False,
			zeroline=False,
			fixedrange=False,
			showticklabels=False
		),
		yaxis=dict(
			range = [min(list(data.data.tail(n=10).Price))-Config.ranj*min(list(data.data.tail(n=10).Price)), max(list(data.data.tail(n=10).Price))+Config.ranj*max(list(data.data.tail(n=10).Price))],
			showline=False,
			fixedrange=True,
			zeroline=False,
		),
		margin=go.Margin(
			t=45,
			l=100,
			r=100,
			b=50,
		)
	)

	basedata=[trace]

	'''Checks for the Checkboxes to add a trace to the graph'''
	if Config.input1 % 2 != 0 :
		move = data.moving_average('Price')
		
		movave = go.Scatter(
			y=move.tail(n=10).Price,
			x=move.tail(n=10).index,
			line=go.Line(
				color='#00695c'
			),
			hoverinfo='skip',
			mode='lines+markers'
		)
		
		basedata.append(movave)

	return go.Figure(data=basedata, layout=layout)

'''Callback fot the subplot
Updates with the placeholder
X axis is the data's one to have a clean subplot
'''
@app.callback(Output('standartdev-graph', 'figure'), [Input('placeholder', 'children')])
def gen_second_graph(interval):
	var = data.percent('Price')

	trace = go.Bar(
		y=var.tail(n=10).Price,
		x=var.tail(n=10).index,
		width = [3000 for i in range(len(var.tail(n=10)))],
		marker=go.Marker(
			color=['#009688' if var.tail(n=10).Price[i]>0 else '#b71c1c' for i in range(len(var.tail(n=10)))]
		),
		hoverinfo='Δ%',
	)

	layout = go.Layout(
		height=200,
		xaxis=dict(
			range = [data.data.tail(n=10).index.min(), data.data.tail(n=10).index.max()],
			showgrid=True,
			showline=True,
			zeroline=False,
			fixedrange=False,
			title='Test'
		),
		margin=go.Margin(
			t=0,
			l=100,
			r=100
		)
	)

	return go.Figure(data=[trace], layout=layout)



'''Callback of the checkboxes'''
@app.callback(Output('test','children'),[Input('movave','value')])
def f(value):
	print (Config.input1)
	if Config.input1%2 == 0:
		yep ='on'
	else:
		yep ='off'

	Config.input1 = Config.input1 + 1
	return yep








'''Internet Status callback
Checks if it can request the <head> of google.com.
It's faster than trying to scrape the whole page
'''
@app.callback(Output('internet-status-graphs', 'children'), events=[Event('internet-update', 'interval')])
def check_connection():
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return 'Status: Online'
	except:
		conn.close()
		return 'Status: Offline'









'''
dcc.Checklist(
		className='checkbox',
		options=[
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montréal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		],
		values=['MTL', 'SF'],
		labelStyle={'display': 'inline-block'}
	),


@app.callback(Output('main-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def gen_price(interval):
	request = WebRequest(kraken, [div,span])
	price, name, time = request.csv_request('final.csv')
	
	data.add_data({'Price':[price],'Tag':[name],'Time':[time]})
	var = data.time_stdv('30S','Price')
	
	
	trace = go.Scatter(
		y=data.data.tail(n=10).Price,
		x=data.data.tail(n=10).index,
		line=go.Line(
			color='#009688'
		),
		hoverinfo='skip',
		mode='lines+markers'
	)

	trace2 = go.Scatter(
		y=var.tail(n=3).Price,
		x=var.tail(n=3).index,
		line=go.Line(
			color='#004d40'
		),
		hoverinfo='skip',
		mode='lines+markers'
	)

	fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=False)
	fig.append_trace(trace, 1, 1)
	#fig.append_trace(trace2, 2, 1)

	fig['layout']['xaxis1'].update(range=[data.data.tail(n=10).index.min(),data.data.tail(n=10).index.max()])
	fig['layout']['yaxis1'].update(range=[min(list(data.data.tail(n=10).Price))-Config.ranj*min(list(data.data.tail(n=10).Price)), max(list(data.data.tail(n=10).Price))+Config.ranj*max(list(data.data.tail(n=10).Price))])
	#fig['layout']['xaxis2'].update(range=[var.tail(n=3).index.min(), var.tail(n=3).index.max()])
	#return go.Figure(data=[trace,trace2], layout=layout)
	return fig
'''