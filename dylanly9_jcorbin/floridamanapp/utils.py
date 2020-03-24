"""
Form utilities for the web app.
"""
from collections import namedtuple
from textwrap import indent, dedent
from enum import Enum, auto

class FormInputs(Enum):
    STRING = auto()
    TEXTAREA = auto()
    NUMERIC = auto()
    FILE = auto()

def get_input_elem(*args):
    name, label, f_type, default = args

    picker_type = isinstance(f_type, list) \
                  or isinstance(f_type, set) \
                  or isinstance(f_type, tuple)
    if picker_type:
        output = (f"<select multiple class='form-control' id='{name}'"
                  f" name='{name}'>")
        for option in f_type:
            if default and option in default:
                output += f"\n  <option selected>{option}</option>"
            else:
                output += f"\n  <option>{option}</option>"
        output += "\n</select>"
        return output

    elif f_type is FormInputs.NUMERIC:
        return (f"<input type='number' class='form-control' id='{name}'"
                f" name='{name}' value='{default or ''}' />")

    elif f_type is FormInputs.TEXTAREA:
        return (f"<textarea class='form-control' id='{name}' name='{name}'>"
                f"{default or ''}</textarea>")

    elif f_type is FormInputs.FILE:
        return (f"<input type='file' class='custom-file-input' id='{name}'"
                f" name='{name}' value='{default or ''}' />")

    else:
        # Treat as a string type
        return (f"<input class='form-control' id='{name}' name='{name}'"
                f" value='{default or ''}' />")

class Form:
    def __init__(self, form_spec, defaults={}):
        self._form_spec = form_spec
        self.fields = []

        for name, spec in form_spec.items():
            self.fields.append(FormField(name, *spec, defaults.get(name)))

    def __iter__(self):
        return iter(self.fields)

BaseField = namedtuple('BaseField', ('name', 'label', 'f_type', 'default'))
class FormField(BaseField):
    def render(self):
        input_elem = indent(get_input_elem(*self), '  ')

        group_class = 'form-group'
        label_class = ''
        if self.f_type is FormInputs.FILE:
            group_class = 'custom-file'
            label_class = 'custom-file-label'

        return dedent(f"""\
        <div class='{group_class}'>
          <label for='{self.name}' class='{label_class}'>{self.label}</label>
          {input_elem}
        </div>
        """)
