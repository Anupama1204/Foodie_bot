from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import AllSlotsReset
from rasa_core.events import Restarted
import zomatopy
import json

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	@staticmethod        
	def cities_db():
		print("**********Inside  Cities DB  ************")          
		return['ahmedabad', 'bangalore', 'chennai', 'delhi', 'hyderabad', 'kolkata', 'mumbai', 'pune', 'agra', 'ajmer', 'aligarh', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bokaro steel city', 'chandigarh', 'coimbatore', 'cuttack', 'dehradun', 'dhanbad', 'durg-bhilai nagar', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur', 'gulbarga', 'guntur', 'gurgaon', 'guwahati','gwalior', 'hubli-dharwad', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kannur', 'kanpur', 'kakinada', 'kochi', 'kottayam', 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'lucknow', 'ludhiana', 'madurai', 'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nagpur', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 'pondicherry', 'prayagraj', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur', 'srinagar', 'sultanpur', 'surat', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tirunelveli', 'tiruppur', 'ujjain', 'bijapur', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'visakhapatnam', 'warangal','bombay','madras','calcutta','gautam budh nagar','new delhi','hydrabad','bengaluru','bengalore','ahemdabad']
    
	@staticmethod
	def cuisines_db():
		print("**********Inside Cuisines DB  ************")  
		return['american','italian','chinese','mexican','north indian','south indian']
    
#	def validate_slots():
#		print("**********Inside  Validation ************")        
#		loc=tracker.get_slot('location')
#		cuisine=tracker.get_slot('cuisine')
#		if loc not in self.cities_db():
#			dispatcher.utter_template("utter_wrong_city",tracker)
#			SlotSet(location,None)
#			return[False]
#		if cuisine not in self.cuisines_db():
#			dispatcher.utter_template("utter_wrong_cuisine",tracker)
#			SlotSet(cuisine,None)
#			return[False]

#		return[True]                    
        
        
	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"487f59f967d831d0137ed79b92c3fc2f"}
		zomato = zomatopy.initialize_app(config)
		print("Latest user message : ",tracker.latest_message.text)
		loc=tracker.get_slot('location')
		cuisine=tracker.get_slot('cuisine')
		if cuisine not in self.cuisines_db():      
			print("Wrong Cuisine")            
			dispatcher.utter_template("utter_wrong_cuisine",tracker)
			SlotSet('cuisine',None)
		elif loc not in self.cities_db():
			dispatcher.utter_template("utter_wrong_city",tracker)
			SlotSet('location',None)
		else:
			loc = tracker.get_slot('location')
			print("Location identified is : ",loc)
			print("Cuisine identified is : ",cuisine)
			cuisine = tracker.get_slot('cuisine')
			location_detail=zomato.get_location(loc, 1)
			d1 = json.loads(location_detail)
			lat=d1["location_suggestions"][0]["latitude"]
			lon=d1["location_suggestions"][0]["longitude"]
			cuisines_dict={'american':1,'chinese':25,'mexican':73,'italian':55,'north_indian':50,'south_indian':85}
			results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
			d = json.loads(results)
			response=""
			if d['results_found'] == 0:
				response= "no results"
			else:
				for restaurant in d['restaurants']:
					response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"

			dispatcher.utter_message("-----"+response)
			SlotSet('location',None)
			SlotSet('cuisine',None)
		return [SlotSet('location',None),SlotSet('cuisine',None)]

