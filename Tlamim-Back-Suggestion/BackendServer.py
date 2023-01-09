from sql.SqlServer import SqlServer
from email.EmailServer import EmailServer
from forms.FormsServer import FormsServer


class BackendServer(object):

    def __init__(self):
        pass

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


