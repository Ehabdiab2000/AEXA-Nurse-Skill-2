import os
import boto3

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from commons import CommonFunctions

ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')

ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)

messages = {
    'welcome' : 'Hello, Please give me your name',
    'name_reprompt' : 'Please give me your name',
    'ask_age' : 'Please give me your age',
    'ask_height' : 'Please give me your height in feets',
    'ask_weight' :'Please give me your weight in kilograms',
    'ask_temperature':'Please give me your temperature in degree celsius',
    'ask_complain' : 'You are welcome #NAME#, what is your complain?',
    'accident_message':'Please check with nurse immediately',
    'contact_hamad' : 'Please check with doctor Hamad',
    'contact_mera' : 'Please go to doctor Mera',
    'help' : 'What is your complain?',
    'fallback' : 'Sorry I didnt unerstand that. Can you repeat?',
    'stop' : 'Goodbye'

}

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        speech = messages['welcome']
        reprompt = messages['name_reprompt']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'name', 'NameIntent')


class CaptureNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NameIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        name = slots["name"].value
        sessionAttributes['user_name'] = name
        speech = messages['ask_age']
        reprompt = messages['ask_age']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'age', 'AgeIntent')

class CaptureAgeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AgeIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        age = slots["age"].value
        sessionAttributes['user_age'] = age
        speech = messages['ask_weight']
        reprompt = messages['ask_weight']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'weight', 'WeightIntent')

class CaptureWeightIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("WeightIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        weight = slots["weight"].value
        sessionAttributes['user_weight'] = weight
        speech = messages['ask_height']
        reprompt = messages['ask_height']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'height', 'HeightIntent')

class CaptureHeightIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HeightIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        height = slots["height"].value
        sessionAttributes['user_height'] = height
        speech = messages['ask_temperature']
        reprompt = messages['ask_temperature']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'temperature', 'TemperatureIntent')

class CaptureTemperatureIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("TemperatureIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        temperature = slots["temperature"].value
        sessionAttributes['user_temperature'] = temperature
        speech = messages['ask_complain'].replace('#NAME#', sessionAttributes['user_name'])
        reprompt = messages['help']
        return CommonFunctions.sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, 'complain', 'ComplainIntent')

class CaptureComplainIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ComplainIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        complain = slots["complain"].value
        sessionAttributes['complain'] = complain
        if complain == 'accident':
            speech = messages['accident_message']
            return CommonFunctions.sendStopResponseToAlexa(self, handler_input, speech)
        if int(sessionAttributes['user_temperature']) >= 38:
            speech = messages['contact_hamad']
            bookAppointment = CommonFunctions.bookAppointment(sessionAttributes, 'HAMAD')
            return CommonFunctions.sendStopResponseToAlexa(self, handler_input, speech)
        speech = messages['contact_mera']
        bookAppointment = CommonFunctions.bookAppointment(sessionAttributes, 'MERA')
        return CommonFunctions.sendStopResponseToAlexa(self, handler_input, speech)


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        speech = messages['help']
        reprompt = messages['help']
        return CommonFunctions.sendResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt)

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
       speech = messages['stop']
       return CommonFunctions.sendStopResponseToAlexa(self, handler_input, speech)

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        sessionAttributes = handler_input.attributes_manager.session_attributes
        speech = messages['fallback']
        reprompt = messages['fallback']
        return CommonFunctions.sendResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt)

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):   
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


sb = sb = CustomSkillBuilder(persistence_adapter = dynamodb_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CaptureNameIntentHandler())
sb.add_request_handler(CaptureAgeIntentHandler())
sb.add_request_handler(CaptureHeightIntentHandler())
sb.add_request_handler(CaptureWeightIntentHandler())
sb.add_request_handler(CaptureTemperatureIntentHandler())
sb.add_request_handler(CaptureComplainIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) 

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()