
'''
Appending css and creating the dash element for the app
Located in a another file to share it with the other pages
'''
import dash

app = dash.Dash(__name__)

for i in ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css"]:
	app.css.append_css({"external_url": i})


server = app.server
app.config.suppress_callback_exceptions = True

