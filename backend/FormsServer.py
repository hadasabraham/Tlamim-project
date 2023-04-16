from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools, clientsecrets
from dateutil.parser import parse
import os
import pathlib

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


class FormServer(object):
    def __init__(self, token_path="form_token.json", credentials_path="form_credentials.json"):

        store = file.Storage(token_path)
        creds = None
        if store:
            creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(str(pathlib.Path(__file__).parent.resolve()) + os.path.sep + credentials_path,
                                                  SCOPES)
            creds = tools.run_flow(flow, store)

        self.__form_service = discovery.build('forms', 'v1', http=creds.authorize(Http()),
                                              discoveryServiceUrl=DISCOVERY_DOC,
                                              static_discovery=False)

    def get_form_structure(self, form_id):
        form_structure = self.__form_service.forms().get(formId=form_id).execute()
        return form_structure

    def get_form_responses(self, form_id: str, last_response: str):
        if last_response:
            responses = self.__form_service.forms().responses().list(formId=form_id,
                                                                     filter=f"timestamp > {last_response}").execute()
        else:
            responses = self.__form_service.forms().responses().list(formId=form_id).execute()

        return responses


class FormDecoder(object):

    @staticmethod
    def get_questions_answers(response: dict, form_structure: dict):
        timestamp, email, answers = FormDecoder.get_form_answers(response=response)
        questions = FormDecoder.get_form_questions(form_structure=form_structure)
        return FormDecoder.match(form_questions=questions, form_answers=answers)

    @staticmethod
    def get_form_questions(form_structure: dict) -> list[tuple[str, str]]:
        """
        Decodes a given form structure;
        :param form_structure: the form structure as received from the google-form api
        :return: list of (question_id, question_title) pairs
        """

        res = []
        for item in form_structure['items']:
            question_title = item['title'].strip()
            question_item = item['questionItem']
            question = question_item['question']
            question_id = question['questionId']
            pair = (question_id, question_title)
            res.append(pair)
        return res

    @staticmethod
    def get_form_answers(response: dict) -> tuple[str, str, list[tuple[str, str]]]:
        """
        Decodes a given form response;
        :param response: the form response as received from the google-form api
        :return: (email, timestamp, [(question_id, question_answers) pairs])
        """
        timestamp = response['lastSubmittedTime']
        email = str(response['respondentEmail'])
        answers = []

        for q_id, q_item in response['answers'].items():
            if 'textAnswers' in q_item.keys():
                text_answers = q_item['textAnswers']['answers'][0]['value'].strip()
                answers.append((q_id, text_answers))

        return email, timestamp, answers

    @staticmethod
    def match(form_questions: list[tuple[str, str]], form_answers: list[tuple[str, str]]) -> list[tuple[str, str]]:
        """
        Matches the questions to the answers;
        :param form_questions: as received by get_form_questions
        :param form_answers: as received by get_form_answers
        :return: list of (question_title, answer) pairs
        """
        res = []
        for q_id1, q_title in form_questions:
            for q_id2, q_ans in form_answers:
                if q_id1 == q_id2:
                    pair = (q_title, q_ans)
                    res.append(pair)
        return res
