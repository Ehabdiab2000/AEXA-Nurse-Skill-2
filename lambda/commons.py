from ask_sdk_model.dialog import ElicitSlotDirective
from ask_sdk_model import (
    Intent, IntentConfirmationStatus, Slot, SlotConfirmationStatus)

from db import DynamoDBLayer
from datetime import date
import pytz
from datetime import datetime

class CommonFunctions:

    def sendResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt):
        updateAttributes(self, handler_input, sessionAttributes)
        return (
            handler_input.response_builder.speak(speech)
            .set_should_end_session(False)
            .ask(reprompt)
            .response
        )
    
    def sendStopResponseToAlexa(self, handler_input, speech):
        return (
            handler_input.response_builder.speak(speech)
            .set_should_end_session(True)
            .response
        )

    def sendElictSlotResponseToAlexa(self, handler_input, sessionAttributes, speech, reprompt, slotToElict, intentToElicit):
        updateAttributes(self, handler_input, sessionAttributes)
        directive = ElicitSlotDirective(
        slot_to_elicit=slotToElict,
        updated_intent=Intent(
            name=intentToElicit,
            confirmation_status=IntentConfirmationStatus.NONE,
            slots={
                    slotToElict: Slot(
                        name=slotToElict,
                        confirmation_status=SlotConfirmationStatus.NONE)
                }
            )
        )
        return(
            handler_input.response_builder.speak(speech)
            .set_should_end_session(False)
            .ask(reprompt)
            .add_directive(directive)
            .response
        )
    

    def bookAppointment(sessionAttributes, doctor):
        appointment_time = getCurrentDateTime()
        putAppointment = DynamoDBLayer.putAppointment(doctor, sessionAttributes, appointment_time)
        return

  
def updateAttributes(self, handler_input, sessionAttributes):
    handler_input.attributes_manager.session_attributes = sessionAttributes
    # handler_input.attributes_manager.save_persistent_attributes()
    return


def getCurrentDateTime():
    current_time = pytz.timezone('Asia/Dubai')
    current_time_format = datetime.now(current_time)
    return current_time_format.strftime("%Y-%m-%d %H:%M:%S")
    
    