'''
Main layout, redirects the user depending on the URL

'''

from __init__ import version
print('app_version ',version)
print('started import')
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from pages.modules.config import Config
from pages import graphs, projet, internet
from pages.app import app
print('finished import')


'''Body of the html located in the div, location checks for the url'''
app.layout = html.Div(id='bg', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={} , children=graphs.LAYOUT)
])


'''Network Layout
Using Dash callbacks with the location as input
'''
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graphs':
        return graphs.LAYOUT
    
    elif pathname == '/projet':
        return projet.LAYOUT
    
    elif pathname == '/internet':
        return internet.LAYOUT
    
    else:
        return html.A(href='/graphs', children='Redirect to graphs')


'''App Launch'''
if __name__ == '__main__':
    app.run_server(debug=True)

