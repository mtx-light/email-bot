import re

with open('./smiddle_products/utils/aggressive.txt') as f:
    words = {w.lower().strip() for w in f.readlines()}


def is_aggressive(text):
    text = re.sub('\!\?\,\;\.', '', text).lower().split(' ')
    for w in text:
        if w in words:
            return True
    return False

def aggressive_filter(state):
    def _state(request, responder):
        if not is_aggressive(request.text):
            state(request, responder)
        else:
            responder.frame["aggressive_count"] = responder.frame.get("aggressive_count", 0) + 1
            if responder.frame["aggressive_count"] > 2:
                responder.frame["aggressive_count"] = 0
                responder.reply("Успокойтесь, мы соееденим вас с оператором.")
            else:
                responder.reply("Успокойтесь, пожалуйста, мы решим вашу проблему.")
    _state.__name__ = state.__name__
    return _state