import random
from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_START_QUIZ = "ask_question"
INTENT_ANSWER = "give_answer"
INTENT_DOES_NOT_KNOW = "does_not_know"
INTENT_GIVE_NAME = "give_name"

INTENT_FILTER_GET_ANSWER = [
    INTENT_ANSWER,
    INTENT_DOES_NOT_KNOW
]

current_questions = {}

def user_request_question(hermes, intent_message):
    x = random.randint(0, 12)
    y = random.randint(0, 12)
    sentence = "What is {} times {} ?".format(x, y)
    print(sentence)

    current_questions[intent_message.session_id] = {"x": x, "y": y}

    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

def user_does_not_know(hermes, intent_message):
    sentence = "User does not know"
    print(sentence)

    hermes.publish_end_session(intent_message.session_id, sentence)

def user_gives_answer(hermes, intent_message):
    question = current_questions[intent_message.session_id]
    x = question["x"]
    y = question["y"]
    answer = x * y
    user_answer = intent_message.slots.answer.first().value.value

    sentence = "{} the answer was {}"

    if (answer != user_answer):
        sentence = sentence.format("No, ", answer)
    else:
        sentence = sentence.format("Indeed, ", answer)

    print(sentence)

    hermes.publish_end_session(intent_message.session_id, sentence)

def session_ended(hermes, session_ended_message):
	pass

def session_started(hermes, session_started_message):
	pass

with Hermes(MQTT_ADDR) as h:

    h.subscribe_intent(INTENT_START_QUIZ, user_request_question) \
        .subscribe_intent(INTENT_DOES_NOT_KNOW, user_does_not_know) \
        .subscribe_intent(INTENT_ANSWER, user_gives_answer) \
        .subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()
