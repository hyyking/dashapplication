'''
Internet page, displays the config
'''

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import http.client as httplib
from .app import app


from .modules.config import Config

'''Navbar from materializeCSS
One callback for the internet update'''
header=html.Nav(children=[
	html.Div(className='teal nav-wrapper', children=[
		html.A(href='#', className='brand-logo right', children='Application'),
		html.Ul(id='nav-mobile', className='left hide-on-med-and-down', children=[
			html.Li(children=[html.A(href='/graphs', children='Graphs')]),
			html.Li(children=[html.A(href='/projet', children='Project')]),
		])
	]),
])


'''Basic content displaying the config'''
content=html.Div(style={'padding':'0px 10px 15px 10px'}, children=[
	html.Table(children=[		
		html.Tr(children=[
			html.Td(style={'width':'40%', 'margin-right':'100px'}, children=[
				html.H5(style={'padding-left':'50px'}, id='status-content')
			]),
			html.Td(style={'width':'40%', 'margin-right':'100px'}, children=[
				html.H5(id='status-update-speed', children='Updating speed: '+str(Config.internet_status_update)+'s')
			])
		])
	])
])

'''All the updates'''
updates=html.Div(children=[
	dcc.Interval(id='internet-update', interval=Config.internet_status_update*1000),
])


'''Compacted layout for usage in main.py
Also contains the styling of the layout of the app'''
LAYOUT = html.Div(style={'backgroundColor':'#FFFFFF','marginLeft':'auto','marginRight':'auto',"width":"70%",'boxShadow':'0px 0px 5px 5px rgba(204,204,204,0.4)'}, children=[header, content, updates])

'''Internet update checks if it can get hold of the <head> of google.com'''
@app.callback(
	Output('status-content', 'children'),
	events=[Event('internet-update', 'interval')
])
def connexion_status():
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return 'Status: Online'
	except:
		conn.close()
		return 'Status: Offline'



