"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

This README is old so better explanation for the tables structure can be found within the SqlServer.py file .
This version is saved to allow contemplating the pros and cons for the new structure and to allow
to consider which function have to be implemented to the mvp.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


"""

To fulfill MVP with this suggestion have to implement all forms server and its decoders,
the sql server without the general search (I am not sure what It's supposed to do and how), close stage, load and export.
But have to enable adding entries to each table.
Must add wrappers to get_* in the backend server to allow the backend app send relevant data to the frontend
and the wrapper to the add_stage that is necessary to initialize the system (changes to stages still not allowed).

Have to implement the backend server refresh_database using the forms server and the sql server to retrieve
all answers and candidates and update the database.
Have to implement the start cycle as just creating table and clear all databases (load from future use still not allowed).

Have to implement the backend server notify_frontend_head to show that we can notify about candidate who waits for decisions
and prove that our system can help.
Currently, I assume that ones in a while a request to notify about waiting candidates is done by the frontend.

Don't have to implement the email server and the notify_candidates and notify_frontend_all of the backend server.

In the frontend app have to implement a suitable url for each backend server functionality that can be called by the frontend.
Meaning url for the get_* wrappers, notify_frontend_head and maybe url for add_stage if the frontend support such page, and we
won't initialize the stages table manually.

"""

"""
The credentials for the forms and gmail api should be stored in the appropriate folders.
Probably should save them encrypted or something else.

Notice that most of the answers, questions and other data saved as text in hebrew.
When sending a list[dict] that represents json as a response to the frontend we need to


# for each stage save the index in the sorting process, stage name, the form_id associated with the stage and form link to send to candidates
Stages(stage_index INTEGER PRIMARY KEY, stage_name TEXT, form_id TEXT, form_link TEXT)

Notice that the stage with index 0 is the initial stage when the candidate submit his initial application.
Notice that each stage can have multiple forms but each form can be used only to a single stage


# for each candidate save his unique email, first and family name and current stage index.
# In addition we save the current status of candidate such as didn't complete stage, wait for grading, waiting for decision etc.
# The status for those who failed to pass a stage (regardless the reason) becomes eliminated.
CandidatesGeneralInformation(email TEXT PRIMARY KEY, first_name TEXT, family_name TEXT, current_stage_index INTEGER,
                                                                                        current_status TEXT)


# for each form_id that mach to stage_index and filled by the candidate_email save the response as a json string
CandidatesAnswers(stage_index TEXT, form_id TEXT, candidate_email TEXT, response TEXT, PRIMARY KEY(form_id, candidate_email))

# IMPORTANT IDEA !!!!
# If we will save the response in the CandidatesAnswers table as a json text in the format [{'title':'<question-title>', 'answer':'<question-answer>'}]
# instead of the Google forms full response format we will be able to export and load data to table
# with the questions as columns as long the table has email and stage_index columns as well
# and the stages table hasn't changed (More explanation about those problem comes at the cons section).
# However with this suggestion have to add timestamp colum to the CandidatesAnswers table, so we can update responses currently, and it won't be
# saved in the new response format.
# Using stage_index and form_id allows to load data that haven't come from a Google form but has q suitable structure while allowing
# future compatibility if we wish to mach more than one form to a stage.
# It can help to the loading data from stage 0 that I don't sure if it comes from a form or on other way.
# Notice that stage without form-id can't update its relevant data but manually (or by manually asking to load some csv)
# and it is never going to be updated by the Google forms api.

# for each stage and candidate save the grade given on the stage and general notes on the stage
Grades(stage_index INTEGER, candidate_email TEXT, grade FLOAT, notes TEXT, PRIMARY KEY(stage_index, candidate_email))


# for each candidate save which stages he passed and optional notes.
Decisions(stage_index INTEGER, candidate_email TEXT, pass BOOL, notes TEXT, PRIMARY KEY(stage_index, candidate_email))

Notes:
    if the candidate accepted to the program he has pass==1 with stage_index==last_stage
    When eliminating a candidate if the frontend requests to save his information (i.e. export it)
    all the candidates relevant rows from each table saved to some other similar database for future use.

    At the beginning of the selection process we clear all the Tables but the Stages table.
    We allow to the frontend to change the stages on demand.
    If there was no change the future use database can be loaded to the main database, and we clear all of its tables.
    The loaded candidates can start from where they stopped (eliminated).

    If there was a change than the backend allows to send all the saved candidates an email
    with the new selection process and start it from scratch.
    If there was a change than the stages table being cleared or changed relative to the demanded change.
    After suggesting restart the process to the future use candidates we clear all its tables.

"""


"""

Pros:
    * Can export and load csv given the tables saved as is.

    * Given that the selection process didn't change can save candidates for next cycles
      and load them in the future into the database.

    * Can export the data to table with questions titles as columns and the answers in the rows (Eleazar current format).

    * Saving small amount of data in the CandidatesGeneralInformation allows flexibility to change the process
      without changing the tables structure (Most of the data saved as jsons text).

    * Stages, Decisions and Grades are the only tables that we manually inset data to and those are tables that
      we wish the frontend be able to change.
      We wish to allow changing the stages content/order.
      We wish to allow grading only according to frontend requests.
      We wish to allow decisions (passed/failed) only according to frontend requests.

    * All the tables are updated dynamically except of the stages table that can be updated at
      the start of each cycle.

Cons:
    * Can't load data that was exported in different format from the main format.

    * If the export done to questions-answers format it can't be loaded even if the selection process haven't changed.
      Meaning that can't use Eleazar current tables but if the data was collected by some google forms
      we can use forms api to collect all the responses and insert them to the tables.

    * If the selection process changed can't load old data that exported in any format.

    * Can't update the stages during cycle without hurt the consistency of the system.

"""
