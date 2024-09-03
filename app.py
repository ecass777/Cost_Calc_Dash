from dash import Dash

app = Dash( __name__ ,suppress_callback_exceptions=True,  
           title= "Cloud Cost Calculator",
             external_stylesheets=['https://use.fontawesome.com/releases/v5.7.2/css/all.css',
                                   'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'],
           )