"""
A lightweight Flask app that renders a form for a user to fill out and then
processes the form data with a student-specified function.

Authors
-------
TODO :)
"""
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils import FormInputs
import utils
import process
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

"""
Use these global variables to configure the application parameters.
"""
APP_TITLE = 'OpenDNA'            # Appears at the top of the page.
AUTHORS = 'Daniel Marin'              # Appears underneath the title
FORM_DESCRIPTION = """Welcome to OpenDNA. This program lets you compare your DNA with other users in the database. We'll tell you whose DNA is more similar to yours and add you to our database!!""" # Appears before the form, to explain the form

"""
Use this variable to design the form that you'd like to present the user with.
This dictionary should be of the form:
    {
        'field_name': ('Field Label', field_type)
    }

The field type is one of the following options:
    FormInputs.STRING   -- A string input area.
    FormInputs.TEXTAREA -- A textarea for large string inputs.
    FormInputs.NUMERIC  -- A numeric input area.
    FormInputs.FILE     -- A file upload input.
or an iterable of valid inputs that will be provided to the user to choose
between.

For example, if you were predicting housing prices, this form might look like:
    {
        'age': ('Age', FormInputs.NUMERIC),
        'living_area': ('Size (in square feet)', FormInputs.NUMERIC)
    }

If you'd like to provide a set of valid inputs, you can do that as you'd expect:
    {
        'location': ('Location', ('Palo Alto', 'Stanford', 'Redwood City'))
    }
"""
FORM_SPECIFICATION = {
    'name': ('Enter your name: ', FormInputs.STRING),
    'age':  ('Age', FormInputs.NUMERIC),
    'dna':  ('DNA', FormInputs.STRING),
    'save': ('Save into database?', ('Yes', 'No'))
}


"""
--------------------------------------------------------------------------------
       You don't need to modify anything below this line, although you're        
                    welcome (and encouraged) to take a look!                    
--------------------------------------------------------------------------------
"""
@app.context_processor
def inject_globals():
    return {
        'title': APP_TITLE,
        'authors': AUTHORS
    }

@app.route('/', methods=['GET', 'POST'])
def main():
    form_defaults = dict(request.form)

    # Handle file save
    FILE_FIELDS = [k for k, v in FORM_SPECIFICATION.items() \
                     if v[1] is FormInputs.FILE]
    for field_name in FILE_FIELDS:
        if field_name in request.files \
           and (file := request.files[field_name]).filename:
            # Save the file
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Update the form values
            form_defaults.update({field_name: save_path})

    msg = None
    if any(form_defaults.values()):
        msg = process.process(**form_defaults)
        
    print(msg)

    form = utils.Form(FORM_SPECIFICATION, defaults=form_defaults)

    return render_template('index.html', 
                           form=form,
                           desc=FORM_DESCRIPTION,
                           msg=msg)

if __name__ == '__main__':
    app.run()
