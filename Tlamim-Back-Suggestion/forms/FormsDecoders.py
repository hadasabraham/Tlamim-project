import ast

"""
All decoders assume to recive some json format.
If the json is a string they translate it to some dictionary. Otherwise, they assume this is a dictionary
"""


class FormsDecoder(object):

    def __init__(self, form):
        if isinstance(form, str):
            form = ast.literal_eval(form)
        self.json = form


class FormsSingleResponseDecoder(object):

    def __init__(self, response):
        if isinstance(response, str):
            response = ast.literal_eval(response)
        self.json = response

    

class FormsResponsesDecoder(object):

    def __init__(self, responses):
        if isinstance(responses, str):
            responses = ast.literal_eval(responses)
        self.json = responses



