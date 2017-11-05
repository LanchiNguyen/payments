from flask import Flask
from flask_ask import Ask, statement, question, session, convert_errors
import http.client
import json

app = Flask(__name__)
ask = Ask(app, "/")

@app.route('/')
def homepage():
    return "hi there, how ya doin?"

def create_coupon(description, timeStart, timeEnd):
	statement1 = str(description) + ' from ' + str(timeStart) + ' to ' + str(timeEnd)
	statement2 = "a week"
	#create coupon with salt
	conn = http.client.HTTPSConnection("api.devexhacks.com")

	payload = "{\n  \"title\": \"30% off\",\n  \"callbacks\": {\n    \"couponClickedUrl\": \"https://someurl-couponclicked\",\n    \"couponPresentedUrl\": \"https://someurl-couponpresented\"\n  },\n  \"chainName\": \"Peet's Coffee\",\n  \"description\": \"30% off any purchase from 12pm to 3pm\",\n  \n  \"isStoreWide\": true,\n  \"expirationDate\": \"2017-09-30\",\n  \"isRedeemableInStore\": true\n}"
	coupon_details = json.loads(payload)
	#the salt
	coupon_details["title"] = "coffeejustinwantstolearn"
	coupon_details["description"] = statement1
	coupon_details["expirationDate"] = statement2
	payload = json.dumps(coupon_details)

	headers = {
	    'content-type': "application/json",
	    'accept': "application/json",
	    'authorization': "Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwicGNrIjoxLCJhbGciOiJkaXIiLCJ0diI6Miwia2lkIjoiYTdxIn0..Jn908J-yYgcKMNJnBlhrJg.J15niJBubgAPK5cSeKL6g78C1yBxirQW9HKZ0k1usVdsFOWY392OlR_qUazosk6EiCW2ge-4ahSUo5x-qooNPNz7bb2hWAXmj4MY81oF3oLMHi6JcAPzjYsVHlZQsAYEKjyUCFR7h8h4WHNSukDgidJ6fqumOHflRWCex_eODLYGlJl-B5ksgMByssOZCOFNX-l8ylDscykKpj79steWwPI_mscsEszAbihjXIliQNw7ysEp0Xyxypcc3YCshYIbVpWNcvA1gvmXPeeC4BB0EhwMbtkPdKHAPohnH-Y0y2xJfqQJ64-sG_k_vIIryQTrzQS_cBDldnvbHWWjR1DdJ0B4bFlQz4ciiIt0j7TH6jJPdWPUzII5mKweoNNrSxtkiR0U5ZHPsOuh9dMB7dlaYJQEDm9f4bm8RGoVyLN4NHBhAGL2LAkwCQ7osIVxEvP5nfeP9qZsZTCzQGzvT-a0V8MycVPxAbP1Nem9BV4oY9SbtVaTCwZv948gYOnNEAGW.ysGRHpe2a1rWDtGh30nRdw",
	    'cache-control': "no-cache",
	    'postman-token': "de7eaaa7-6893-dc7f-a60a-0fad30b0834f"
	    }

	conn.request("POST", "/retail-discounts/coupons", payload, headers)

	res = conn.getresponse()
	data = res.read()

@ask.launch
def start_skill():
    welcome_message = 'Got it, what would you like to know?'
    return question(welcome_message)

@ask.intent("BusyIntent")
def ask_busyhours(timeframe):
	if timeframe is None:
		return question("What is the time window you would like to know for Starbucks's busiest hours?") \
			.reprompt("I didn't get that. What is the time window you would like to know for Starbucks's busiest hours?")
	else:
		if timeframe == '1':
			return question('The busiest hour at Starbucks is from 1pm to 2pm')
		elif timeframe == '2':
			return question('The busiest two hours at Starbucks is from 1pm to 3pm')
		elif timeframe == '3':
			return question('The busiest three hours at Starbucks is from 12pm to 3pm')
		elif timeframe == '4':
			return question('The busiest four hours at Starbucks is from 11pm to 3pm')
		elif timeframe == '5':
			return question('The busiest five hours at Starbucks is from 10pm to 3pm')
		else:
			return question('Please give a time window from one hour to five hours')

@ask.intent("HoursIntent")
def ask_timehours(timeframe):
	if timeframe == '1':
		return question('The busiest hour at Starbucks is from 1pm to 2pm')
	elif timeframe == '2':
		return question('The busiest two hours at Starbucks is from 1pm to 3pm')
	elif timeframe == '3':
		return question('The busiest three hours at Starbucks is from 12pm to 3pm')
	elif timeframe == '4':
		return question('The busiest four hours at Starbucks is from 11pm to 3pm')
	elif timeframe == '5':
		return question('The busiest five hours at Starbucks is from 10pm to 3pm')
	else:
		return question('Please give a time window from one hour to five hours')

@ask.intent("CouponIntent")
def ask_coupon():
	return question("Ok, what would you like it to say?")

@ask.intent("CreateCouponIntent")
def ask_createcoupon(description, timeStart, timeEnd):
	# if timeStart < 12:
	# 	timeStart = str(timeStart) + ' in the morning'
	# else if timeStart == 12:
	# 	timeStart = str(timeStart) + ' pm'
	# else:
	# 	timeStart = str(timeStart - 12) + ' in the afternoon'

	# if timeEnd < 12:
	# 	timeEnd = str(timeEnd) + ' in the morning'
	# else if timeEnd == 12:
	# 	timeEnd = str(timeEnd) + ' pm'
	# else:
	# 	timeEnd = str(timeEnd - 12) + ' in the afternoon'

	create_coupon(description, timeStart, timeEnd)
	return question("Ok, I created a coupon for " + str(description) + ' from ' + str(timeStart) + ' to ' + str(timeEnd) + ". Is there anything else you would like me to do?")

if __name__ == '__main__':
    app.run(debug=True)