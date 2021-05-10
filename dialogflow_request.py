from google.cloud import dialogflow
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
project_id_f = open('project_id', 'r')
project_id = project_id_f.read()

language_code = 'ru'

session_client = dialogflow.SessionsClient()

def request(username, text):
    session = session_client.session_path(project_id, username)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return format(response.query_result.fulfillment_text)