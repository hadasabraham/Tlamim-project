from sql.SqlServer import SqlServer
from forms.FormServer import FormServer
from sql.entities.grade import Grade


class BackendServer(object):

    def __init__(self):
        self.__sql_server = SqlServer(database='test_database')
        self.__forms_server = FormServer()
        self.__sql_server.create_tables()

    def get_sql_server(self):
        return self.__sql_server


    def update_grade(self, grade: Grade):
        try:
            self.__sql_server.update_grade(grade=grade)
        except Exception as e:
            print("Got exception", e)

    def save_snapshot(self, snapshot_name: str):
        try:
            self.__sql_server.save_snapshot(snapshot_name=snapshot_name)
        except Exception as e:
            print("Got exception", e)

    def update_candidate_status(self, email: str, status: str):
        try:
            self.__sql_server.update_candidate_status(email=email, status=status)
        except Exception as e:
            print("Got exception", e)

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

