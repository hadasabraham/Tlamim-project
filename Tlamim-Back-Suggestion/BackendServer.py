from sql.SqlServer import SqlServer
from email.EmailServer import EmailServer
from forms.FormServer import FormServer


class BackendServer(object):

    def __init__(self):
        self.__sql_server = SqlServer()
        self.__forms_server = FormServer()
        self.__sql_server.create_tables()

    def get_candidate_summarized(self, email: str) -> list[dict]:
        try:
            return self.__sql_server.get_candidate_summarized(email=email)
        except Exception as e:
            print("Got exception", e)
            return []

    def get_candidate_entire_info(self, email: str) -> list[dict]:
        try:
            return self.__sql_server.get_candidate_entire_info(email=email)
        except Exception as e:
            print("Got exception", e)
            return []

    def search_candidates(self, condition: str) -> list[dict]:
        try:
            return self.__sql_server.search_candidates(condition=condition)
        except Exception as e:
            print("Got exception", e)
            return []

    def refresh_forms_answers(self):
        try:
            forms_info = self.__sql_server.get_forms_required_info_to_adding_answer()
            for _, form in forms_info.iterrows():
                form_id = form['form_id']
                responses_file_type = form['file_type']
                prepared_responses = self.__forms_server.parse_responses_to_add(form_id=form_id, responses_file_type=responses_file_type)
                for form_id, responses_file_type, timestamp, email, prepared_response in prepared_responses:
                    self.__sql_server.add_form_response(form_id=form_id,
                                                        responses_file_type=responses_file_type,
                                                        timestamp=timestamp,
                                                        email=email,
                                                        response=prepared_response)
        except Exception as e:
            print(e)


    def start_new_cycle(self):
        """
        Starting new cycle of candidates by handling the databases and updating the stages table if necessary
        :return:
        """
        pass

    def notify_candidates(self):
        """
        Uses the email server to send all the candidates that didn't respond to there stage form a notification
        :return:
        """
        pass

    def notify_frontend_all(self):
        """
        Uses the database and return all the candidates that have waiting status (wait for response from the selector)
        :return:
        """
        pass

    def notify_frontend_head(self):
        """
        Uses the database and return the first candidate that hase waiting status (wait for response from the selector)
        The order of the candidates is (Time difference from response timestamp till now Descending, stage_index Ascending, Email address Ascending)
        :return:
        """
        pass

    def refresh_database(self):
        """
        Uses the forms server to get all the latest responses of all candidates from all forms and update the database
        :return:
        """
        pass


