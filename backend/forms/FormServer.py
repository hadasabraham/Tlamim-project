from __future__ import print_function
from dateutil.parser import parse
import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools, clientsecrets

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


class FormServer(object):
    def __init__(self, ):

        store = file.Storage(f'{os.getcwd()}{os.path.sep}forms{os.path.sep}token.json')
        creds = None
        if store:
            creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(f'{os.getcwd()}{os.path.sep}forms{os.path.sep}credentials.json',
                                                  SCOPES)
            creds = tools.run_flow(flow, store)

        self.__form_service = discovery.build('forms', 'v1', http=creds.authorize(Http()),
                                              discoveryServiceUrl=DISCOVERY_DOC,
                                              static_discovery=False)

    @staticmethod
    def _get_registration_info(form_structure, response) -> tuple[str, str]:
        pass

    def parse_responses_to_add(self, form_id: str, responses_file_type: str):
        form_structure = self.__form_service.forms().get(formId=form_id).execute()
        responses = self.__form_service.forms().responses().list(formId=form_id).execute()
        res = []
        for response in responses['responses']:
            timestamp = response['lastSubmittedTime']
            email = response['respondentEmail']
            prepared_response = FormServer._prepare_response(response=response, form_structure=form_structure)
            res.append((form_id, responses_file_type, timestamp, email, prepared_response))

        return res

    @staticmethod
    def _get_questions_titles(form_structure):
        res = []
        try:
            items = form_structure['items']
            for item in items:
                keys = item.keys()
                questions = []
                if 'questionItem' in keys:
                    questions = FormServer._parse_question_item(item)
                for question_id, title in questions:
                    res.append((question_id, title))
        except Exception as e:
            print(e)
        finally:
            return res

    @staticmethod
    def _parse_question_item(item) -> list[tuple[str, str]]:
        keys = item.keys()
        if 'title' not in keys:
            return []
        title = item['title']
        question_item = item['questionItem']
        question_item_keys = question_item.keys()
        if 'question' not in question_item_keys:
            return []
        question = question_item['question']

        question_keys = question.keys()
        if 'questionId' not in question_keys:
            return []
        question_id = question['questionId']
        return [(question_id, title)]

    @staticmethod
    def _get_response_answers(questions_info, response) -> list[dict]:
        res = []
        answers = response['answers']
        for q_id, q_title in questions_info:
            question_response = answers[q_id]
            if 'textAnswers' in question_response.keys():
                text_answers = question_response['textAnswers']['answers'][0]['value']  # always have the same structure
                d = dict()
                d['title'] = q_title
                d['answer'] = str(text_answers)
                res.append(d)
            elif 'fileUploadAnswers' in question_response.keys():
                files = question_response['fileUploadAnswers']['answers']
            else:
                continue
        return res

    @staticmethod
    def _prepare_response(response, form_structure) -> list[dict]:
        questions_info = FormServer._get_questions_titles(form_structure=form_structure)

        return FormServer._get_response_answers(questions_info=questions_info, response=response)
