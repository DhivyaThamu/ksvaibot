# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from os import terminal_size
from typing import Any, Text, Dict, List

from requests.models import Response

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import voiceBiometric
import mongo

class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        video_url="https://youtu.be/jj4BL9o3Q7o"
        dispatcher.utter_message("wait... Playing your video.")
        webbrowser.open(video_url)
        return []

class ActionUserDetailsForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        dispatcher.utter_message(response= "utter_name", name =  tracker.get_slot("name"))
        dispatcher.utter_message(response= "utter_number", number =  tracker.get_slot("number"))

        return
class ActionGetDetails (Action):
    def name(self) -> Text:
        return "action_get_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(response= "utter_name", name =  tracker.get_slot("name"))
        dispatcher.utter_message(response= "utter_number", number =  tracker.get_slot("number"))

        return
        
class ActionApplyServices (Action):
    def name(self) -> Text:
        return "action_apply_services"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
     
            service_Type = tracker.get_slot("serviceType")
            cust_name =  tracker.get_slot("name")
            dispatcher.utter_message (response = "utter_serv_type_message", serviceType = service_Type, name = cust_name)
            return

class OpenAccount(Action):
    def name(self) -> Text:
        return "open_account"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        accType = tracker.get_slot("AccType")
        cust_name = tracker.get_slot("name")
        dispatcher.utter_message (text=f"""Glad to help you {cust_name}! Your request is recieved.\n 
                                         To open a new account, please ensure that you have the following documents.\n
                                         1. Address Proof.
                                         2. ID Proof.
                                         3. Passport size photograph.\n
                                         """)
        if (accType != None):
            if (accType.lower() == "savings"):
                dispatcher.utter_message(text = "Check out the links below for more details.")                          
                dispatcher.utter_message(attachment = {
                    "text":"How to open a savings account?",
                    "payload": "https://www.hdfcbank.com/personal/save/accounts/savings-accounts"})
                dispatcher.utter_message(attachment = {
                    "text":"How to open a BSBDA account?",
                    "payload": "https://www.hdfcbank.com/personal/save/accounts/savings-accounts/bsbda-small-account"
                    })
                dispatcher.utter_message(response = "utter_need_assistance")
                return

            elif (accType.lower() == "current"):
                dispatcher.utter_message(text = "Check out the links below for more details.") 
                dispatcher.utter_message(attachment = {
                    "text":"How to open a  Regular Current Account?",
                    "payload":"https://www.hdfcbank.com/personal/save/accounts/current-accounts/regular-current-account"})
                dispatcher.utter_message(attachment = {
                    "text":"How to open a  premium Current Account?",
                    "payload": "https://www.hdfcbank.com/personal/save/accounts/current-accounts/premium-current-account"
                    })
                dispatcher.utter_message(response = "utter_need_assistance")
                return
        dispatcher.utter_message(response = "utter_need_assistance")   
        return


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_details_thanks",
                                 Name=tracker.get_slot("name"),
                                 Mobile_number=tracker.get_slot("number"))
        return
                                 
class ActionAskForEnroll(Action):
    def name(self) -> Text:
        return "action_ask_for_enroll"
    
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("number")
        dispatcher.utter_message(response = "utter_enroll_yourself")
        dispatcher.utter_message(response = "utter_text_to_enroll")
        return

class ActionAskForVerification(Action):
    def name(self) -> Text:
        return "action_ask_for_verification"
    
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("number")
        dispatcher.utter_message(response = "utter_authenticate_yourself")
        dispatcher.utter_message(response = "utter_text_to_authenticate")
        return

class ActionEnroll(Action):
    def name(self) -> Text:
        return "action_biometric_enrollment"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("cust_id")
        Result = voiceBiometric.enrollUser(CustNum)  
        print (f"Result : {Result}") 
        if Result == "Success":
           dispatcher.utter_message(response = "utter_enrollment_success")
           dispatcher.utter_message(response = "utter_text_to_authenticate")
           mongo.Update_enrollment_status(CustNum)
           return [SlotSet("EnrollmentStatus", "success"), SlotSet("BiometricStatus", "Enrolled")]
        else:
            dispatcher.utter_message(text = f"{Result}. Please try again later.")
            dispatcher.utter_message(response = "utter_need_assistance")
            return [SlotSet("EnrollmentStatus", "failed"),  SlotSet("BiometricStatus", "Not Enrolled")]

class ActionVerification(Action):
    def name(self) -> Text:
        return "action_biometric_verification"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("cust_id")
        if CustNum == None:
            dispatcher.utter_message(text =f"This mobile number is not registered with the bank.")
            return[SlotSet("verificationStatus", "failed")]
            
        Result = (voiceBiometric.authenticateUser(CustNum) )
        isRetry = tracker.get_slot("retry")
        print (f"Result : {Result}")
        CurrIntent = tracker.get_slot("currentIntent")
        print(f"Current Intent: {CurrIntent}")
       
        if Result.isdigit():
            score = int (Result)
            if (score < 50) :
                dispatcher.utter_message(f"Verification failed")
                dispatcher.utter_message(response = "utter_need_assistance")
                return[SlotSet("verificationStatus", "failed")]

                
            print(f"Result : {score}") 
            dispatcher.utter_message(f"Verification success.")
            if (CurrIntent == "Fund_Transfer"):
                dispatcher.utter_message(response = "utter_transfer_success")
            elif (CurrIntent == "check_balance"):
                dispatcher.utter_message(response = "utter_account_balance")

            
            dispatcher.utter_message(response = "utter_need_assistance")
            return[SlotSet("verificationStatus", "success")]

        else:
            # Result == "not sufficient voice data":
            dispatcher.utter_message("Verification failed \n  Response from server: " +Result )
            dispatcher.utter_message(response = "utter_need_assistance")
            return[SlotSet("verificationStatus", "failed")]
        
        
class ActionCheckDB(Action):
    def name(self) -> Text:
        return "action_check_db"
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("cust_id")
        if CustNum is None:
                    # The slot is not filled yet. Request the user to fill this slot next.
                    return [SlotSet("requested_slot", "cust_id")]

        Result = mongo.check_cust_status(CustNum)
        print(f"Result: {Result}")
        if Result == "Not Enrolled":
            dispatcher.utter_message(response ="utter_please_enroll")
           
        elif Result == "Enrolled":
            dispatcher.utter_message(response="utter_please_authenticate")
           
        elif Result == "Server Error":
            dispatcher.utter_message(response="Server Connection Failed. Please try later")
           
        else:
            dispatcher.utter_message(response="Customer data not found")
    


class ActionBalanceEnquiry(Action):
    def name(self) -> Text:
        return "action_balance_enquiry"
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        CustNum = tracker.slots.get("number")
        if CustNum is None:
            return [SlotSet("requested_slot", "number")]
        accountBalance = mongo.get_balance(CustNum)
        dispatcher.utter_message(response="utter_account_balance",
                                 Balance = accountBalance)
        # dispatcher.utter_message(message = f"your account balance is {accountBalance}")
        return
class Actionapplyloan(Action):
 
    def name(self) -> Text:
        return "action_get_loan_form_details"
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict]:

        custType = tracker.get_slot('custType')
        print(f"Custtype: {custType}")
        if (custType == "new"):
            return dispatcher.utter_message(response = "utter_ask_number")
        return dispatcher.utter_message(response = "utter_ask_cust_id")
        

class Actionapplyloan(Action):
 
    def name(self) -> Text:
        return "action_Apply_Loan"
 
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict]:

        LoanType = tracker.get_slot('LoanType')
        name=tracker.get_slot('name')

        dispatcher.utter_message(text=f"Glad to assist you. Your request to open {LoanType} Loan is received. Our agent will call you back shortly on your registered mobile number and assist you further.Please make sure that you have the following documents. \n 1. ID Proof. \n 2. Address Proof.\n 3. Passport size Photograph.", name=tracker.get_slot("name"),mobilenumber=tracker.get_slot("number"))
        
        dispatcher.utter_message(response="utter_need_assistance")
        return []
 
class ActionDeposit(Action):
 
    def name(self) -> Text:
        return "action_Deposit"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        
        domain: Dict,
    ) -> List[Dict]:

        name=tracker.get_slot('name')
        dispatcher.utter_message(text=f"Glad to assist you. Please follow these steps. 1.Log in to your net banking or mobile banking service. 2. select the required Deposit type . 3. Enter the OTP received on your registered mobile number. Your request will be processes Successfully.")
        dispatcher.utter_message(attachment = {
                    "text":"https://www.hdfc.com/deposits.",
                    "payload": "https://www.hdfc.com/deposits"
                    })
    
        dispatcher.utter_message(response="utter_need_assistance")
        return

class action_greet(Action):
 
    def name(self) -> Text:
        return "action_greet_user"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        
        domain: Dict,
    ) -> List[Dict]:
        dispatcher.utter_message (response = "utter_greet")
        return
class ActionDeposit(Action):
 
    def name(self) -> Text:
        return "action_set_current_intent"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        
        domain: Dict,
    ) -> List[Dict]:
        intent= tracker.latest_message["intent"].get("name")
        print (f"Current Intent: {intent}")
        return [SlotSet("currentIntent", intent)]