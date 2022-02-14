import os
from mindmeld.components import QuestionAnswerer

APP_NAME = 'smiddle_products'
INDEX_NAME = 'questions'
FILE_PATH = os.path.join('.', APP_NAME, 'data', INDEX_NAME + '.json')

qa = QuestionAnswerer(app_path=APP_NAME)
qa.load_kb(app_namespace=APP_NAME, index_name=INDEX_NAME, data_file=FILE_PATH, clean=True)


def detect_question(state):
    def _state(request, responder):
        answers = qa.get(index=INDEX_NAME, query_type='text', q=request.text)
        if answers and answers[0]['_score'] > 20:
            print(answers[0])
            responder.reply(answers[0]['a'])
            return
        state(request, responder)

    _state.__name__ = state.__name__
    return _state
