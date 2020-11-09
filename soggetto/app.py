import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from sound import audio_sequence
from soggetto import encode_string

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
  html.H6("Change the value in the text box to see callbacks in action!"),
  html.Div(["Input: ",
        dcc.Input(id='my-input', value='Josquin des Prez', type='text')]),
  html.Br(),
  html.Div(id='my-output'),
  html.Br(),
  html.Button('Generate Audio', id='generate-audio', n_clicks=0),
  html.Br(),
  html.Audio(src='../audio/josquin_example.wav', controls=True),
])


# @app.callback(
#   dash.dependencies.Output('container-button-basic', 'children'),
#   [dash.dependencies.Input('generate-audio', 'n_clicks')],
#   [dash.dependencies.State('input-on-submit', 'value')])
# def update_output(n_clicks, value):
#   return 'The input value was "{}" and the button has been clicked {} times'.format(
#     value,
#     n_clicks
#   )


@app.callback(
  Output(component_id='my-output', component_property='children'),
  [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
  solfege, notes = encode_string(input_value)
  #audio = audio_sequence(notes)
  return f"Solfege: {solfege}\nNotes: {notes}"


if __name__ == '__main__':
  app.run_server(debug=True)
