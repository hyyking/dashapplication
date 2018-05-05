'''
Projet page will contain a description of the project
'''

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event	
from .app import app
import http.client as httplib

from .modules.config import Config


'''NavBar from materializeCSS
One callback for the internet update'''
header=html.Nav(children=[
	html.Div(className='teal nav-wrapper', children=[
		html.A(href='#', className='brand-logo right', children='Application'),
		html.Ul(id='nav-mobile', className='left hide-on-med-and-down', children=[
			html.Li(children=[html.A(href='/graphs', children='Graphs')]),
			html.Li(children=[html.A(href='/projet', children='Project')]),
			html.Li(children=[html.A(id='internet-status-projet', href='/internet', children='Status')])
		])
	]),
])


'''Page Content'''
content=html.Div(style={'padding':'0px 10px 15px 10px'}, children=[
	html.H3(children='PROJET')
])

'''Updates'''
updates=html.Div(children=[
	dcc.Interval(id='internet-update', interval= Config.internet_status_update*1000)
])


'''Compacted layout for usage in main.py
Also contains the styling of the layout of the app'''
LAYOUT = LAYOUT = html.Div(style={'backgroundColor':'#FFFFFF','marginLeft':'auto','marginRight':'auto',"width":"70%",'boxShadow':'0px 0px 5px 5px rgba(204,204,204,0.4)'}, children=[header, content, updates])



'''Connexion status callback, trying to get hold of the <head> element of google.com'''
@app.callback(Output('internet-status-projet', 'children'), events=[Event('internet-update', 'interval')])
def check_connection():
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return 'Status: Online'
	except:
		conn.close()
		return 'Status: Offline'
