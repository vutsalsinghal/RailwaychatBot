from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from pytz import timezone
import datetime as dt
from django.core.mail import send_mail

@csrf_exempt
def page(request):
	req = json.loads(str(request.body, 'utf-8'))

	def try_error(code):
		if code == 204:
			d['speech'] = d['displayText'] = 'Not able to fetch required data or there is no data for your query!'
			return False
		elif code == 210:
			d['speech'] = d['displayText'] = "Train doesn’t run on the date queried!"
			return False
		elif code == 220:
			d['speech'] = d['displayText'] = 'Flushed PNR!'
			return False
		elif code == 221:
			d['speech'] = d['displayText'] = 'Invalid PNR supplied!'
			return False
		elif code == 304:
			d['speech'] = d['displayText'] = 'Data couldn’t be fetched. No data available for the given query!'
			return False
		elif code == 403:
			d['speech'] = d['displayText'] = 'Usage Quota for the day exhausted. Sorry for the inconvenience! Please try again after 12AM (IST)'
			return False
		elif code == 404:
			d['speech'] = d['displayText'] = "Sorry, Doesn't Exist! :/"
			return False
		elif code == 405:
			d['speech'] = d['displayText'] = "Data couldn’t be loaded! Request didn't go through."
			return False
		elif code == 500:
			d['speech'] = d['displayText'] = 'Sorry! Unable to process request at this time! Railway API Error Code: 500'
			return False
		elif code == 504:
			d['speech'] = d['displayText'] = 'Argument error!'
			return False
		elif code == 510:
			d['speech'] = d['displayText'] = 'Train not scheduled to run on the given date.'
			return False
		elif code == 704:
			d['speech'] = d['displayText'] = 'Sorry! unable to complete request at the moment. Please try after 12 AM IST.'
			return False
		elif code == 200:
			return True

	if req['result']['action'] == 'train.help':
		if req['result']['metadata']['intentName'] == 'train_help':
			retString = 'What do you need help with?\n\n1. Live status\n2. Train Info & Route\n3. Trains between 2 stations\n4. PNR status\n5. Cancelled trains\n6. Station name auto-complete\n7. Rescheduled trains\n\nPick a number:' #8. Seat availability\n9. Train fare\n10. Trains arrival at a station\n\nPick a number:'
			d = {
				"speech": '',
				"displayText": '',
				"data": {
					"facebook" : {
						"text":"Pick a number:",
						"quick_replies":[
						  {
							"content_type":"text",
							"title":"1",
							"payload":"1"
						  },
						  {
							"content_type":"text",
							"title":"2",
							"payload":"2"
						  },
						  {
							"content_type":"text",
							"title":"3",
							"payload":"3"
						  },
						  {
							"content_type":"text",
							"title":"4",
							"payload":"4"
						  },
						  {
							"content_type":"text",
							"title":"5",
							"payload":"5"
						  },
						  {
							"content_type":"text",
							"title":"6",
							"payload":"6"
						  },{
							"content_type":"text",
							"title":"7",
							"payload":"7"
						  }
						]
					},
					"telegram": {
						"text": 'What do you need help with?\n\n1. Live status\n2. Train Info & Route\n3. Trains between 2 stations\n4. PNR status\n5. Cancelled trains\n6. Station name auto-complete\n7. Rescheduled trains\n\nPick a number:', #8. Seat availability\n9. Train fare\n10. Trains arrival at a station\n\nPick a number:',
						'one_time_keyboard': 'true',
						"reply_markup": {
						  "keyboard": [
								['1','2','3'],
								['4','5','6'],
								['7']
							]
						}
					}
				},
				"contextOut": [],
				"source": "railwaybot.pythonanywhere.com"
				}

			d['data']['facebook']['text'] = retString
			return JsonResponse(d)

		elif req['result']['metadata']['intentName'] == 'train_help_id':
			helpId = req['result']['parameters']['help_id']
			retString = ''
			d = {
				"speech": '',
				"displayText": '',
				"data": {},
				"contextOut": [],
				"source": "railwaybot.pythonanywhere.com"
				}

			if helpId == '1':
				retString = 'To know Live status, some possible statements you can type/speak can be:\n\n#. Live status <train\n Code>\n #. Live status of <train Name/Code> which started <today/yesterday/day before yesterday>\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			elif helpId == '2':
				retString = 'To know Train Info & Route, some possible statements you can type/speak can be:\n\n #. Route of <train/number>\n Info of <train name/number>\n #. Train info of <train name/number>\n #. Train route <train name/number>\n #. Route <train name/number>\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			elif helpId == '3':
				retString = 'To find out trains b/w two stations, some possible statements you can type/speak can be:\n\n #. What are the trains between <src stn> and <dst stn> on <particular date/today/tomorrow etc>\n #. Trains between <src stn> and <dst stn> on <particular date/today/tomorrow etc>\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			elif helpId == '4':
				retString = 'To do PNR enquiry, some possible statements you can type/speak can be:\n\n #. PNR status of 1234567890\n #. PNR status 1234567890\n #. PNR 1234567890\n #. PNR number 1234567890\n #. PNR enquiry 1234567890\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			elif helpId == '5':
				retString = 'To know List of cancelled trains, some possible statements you can type/speak can be:\n\n #. List of cancelled trains\n #. What are the cancelled train <today/tomorrow etc>\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			elif helpId == '6':
				retString = 'To auto-complete a station name/code, some possible statements you can type/speak can be:\n\n #. auto complete station name <partial name>\n #. name of station with <partial name>\n #. suggest station name <partial name>\n #. possible station name <partial name>\n\nThese are just sample statements!\n\nNote: You\'ve to enter partial "station NAME" not "station CODE" such as DEL for DELHI'
				d['speech'] = d['displayText'] = retString

			elif helpId == '7':
				retString = 'To know list of rescheduled trains, possible statements you can type/speak can be:\n\n #. List of  rescheduled trains\n #. What are the rescheduled train <today/tomorrow etc>\n\nThese are just sample statements!'
				d['speech'] = d['displayText'] = retString

			else:
				retString = 'No no no! :D  Try again!\n\n #. Type/speak "help"\n #. Type/speak no. b/w 1 to 7'
				d['speech'] = d['displayText'] = retString
			'''
			elif helpId == '8':
				retString = 'To find seat availability, statements you can type/speak can be: \n\n #. seat availability\n #. seat availability <particular date> on <train name/code> between <src station> and <dst station>'
				d['speech'] = d['displayText'] = retString

			elif helpId == '9':
				retString = 'To find train fare, statements you can type/speak can be: \n\n #. Train fare\n #. Fare of <train name/code> on <particular date> between <src station> and <dst station>\n #. Ticket cost of <train name/code> on <particular date> between <src station> and <dst station>'
				d['speech'] = d['displayText'] = retString

			elif helpId == '10':
				retString = 'To find train arrivals at a station, statements you can type/speak can be: \n\n #. Train arrivals\n #. Train arrivals at <station name/code> within <2 or 4> hours'
				d['speech'] = d['displayText'] = retString
			'''
			return JsonResponse(d)

	elif req['result']['metadata']['intentName'] == 'agent_feedback':
		send_mail('New suggestion on railwaybot.pythonanywhere.com via chatbot', 'Suggestion: ' + req['result']['resolvedQuery'], '', ['pyofey.pythonanywhere@gmail.com'])
		d = {
			"speech": 'Thank you for your valuable feedback!',
			"displayText": 'Thank you for your valuable feedback!',
			"data": {},
			"contextOut": [],
			"source": "railwaybot.pythonanywhere.com"}
		return JsonResponse(d)

	elif req['result']['metadata']['intentName'] == 'train_info':

		retString = 'Some error occured. Maybe try again with different phrase or sentence structure.'
		d = {
			"speech": retString,
			"displayText": retString,
			"data": {},
			"contextOut": [],
			"source": "railwaybot.pythonanywhere.com"}

		date = req['result']['parameters']['date']

		if date == '':
			date = dt.datetime.strptime(req['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		elif date.split('-')[0] == 'UUUU':
			date = date.replace('UUUU', req['timestamp'].split('-')[0])
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		else:
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		'''
		stationNames          = req['result']['parameters']['station-name']
		stationAutoComplete   = req['result']['parameters']['autocomplete-station']
		incompleteStationName = req['result']['parameters']['incomplete-station-name']
		pnr                   = req['result']['parameters']['pnr']
		pnrNumber             = req['result']['parameters']['phone-number']
		liveStatus            = req['result']['parameters']['live-status']
		cancelledTrains       = req['result']['parameters']['cancelled-trains']
		rescheduledTrains     = req['result']['parameters']['rescheduled-trains']
		trainName             = req['result']['parameters']['train-name']
		trainRoute            = req['result']['parameters']['train-route']
		date                  = req['result']['parameters']['date']
		'''
		if req['result']['parameters']['station-name'] != []:
			stationNames = req['result']['parameters']['station-name']

			trainDate = "{0:0=2d}".format(date.day) + "-{0:0=2d}".format(date.month) + "-{0:0=4d}".format(date.year)
			url       = 'http://api.railwayapi.com/v2/between/source/' + stationNames[0] + '/dest/' + stationNames[1] + '/date/' + trainDate + '/apikey/KEY/'
			trainreq  = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ")\n"
					if trainreq['total'] != 0:
						for i in range(trainreq['total']):
							retString += str(i+1) + '. ' + trainreq['trains'][i]['name'] + '(' + trainreq['trains'][i]['number'] + ')\n Travel time: ' + trainreq['trains'][i]['travel_time'] + '\nScr departure time: ' + trainreq['trains'][i]['src_departure_time'] + '\nDst arrival time: ' + trainreq['trains'][i]['dest_arrival_time'] + '\n\n'
					else:
						retString += 'No trains on the above date!'
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)

		elif req['result']['parameters']['pnr'] == 'true':
			#pnr       = req['result']['parameters']['pnr']
			pnrNumber = req['result']['parameters']['phone-number']
			url      = 'http://api.railwayapi.com/v2/pnr-status/pnr/' + str(pnrNumber) +'/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ") " + '\nTrain Name: ' + trainreq['train']['name'] + '(' + trainreq['train']['number'] + ')\nDOJ: ' + trainreq['doj'] + '\nChart Prepared: ' + str(trainreq['chart_prepared']) +'\nFrom station: ' + trainreq['from_station']['name'] + '(' + trainreq['from_station']['code'] + ')' + '\nTo station: ' + trainreq['to_station']['name'] + '(' + trainreq['to_station']['code'] + ')' + '\n\n'
					for i in range(trainreq['total_passengers']):
						retString += 'Passenger no.' + str(i+1) + '\nCurrent Status: ' + trainreq['passengers'][i]['current_status'] + '\nBooking Status: ' + trainreq['passengers'][i]['booking_status'] + '\n\n'
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)			
			return JsonResponse(d)

		elif req['result']['parameters']['live-status'] == 'true':
			trainName = req['result']['parameters']['train-name']

			trainDate = "{0:0=2d}".format(date.day) + "-{0:0=2d}".format(date.month) + "-{0:0=4d}".format(date.year)
			url      = 'https://api.railwayapi.com/v2/live/train/' + trainName + '/date/' + trainDate + '/apikey/KEY/'
			trainreq = requests.get(url).json()
			#d['speech'] = d['displayText'] = trainreq['position']
			#return JsonResponse(d)

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ") \nTrain name: " + trainreq['train']['name'] + '\nPosition: ' + trainreq['position']
					d['speech'] = d['displayText'] = retString
					return JsonResponse(d)
			return JsonResponse(d)

		elif req['result']['parameters']['cancelled-trains'] == 'true':
			#cancelledTrains = req['result']['parameters']['cancelled-trains']
			url      = 'https://api.railwayapi.com/v2/cancelled/date/' + "{0:0=2d}".format(date.day) + '-' + "{0:0=2d}".format(date.month) + '-' + "{0:0=4d}".format(date.year) + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ")\n "
					for i in range(len(trainreq['trains'])):
						retString += str(i+1) + '. ' + trainreq['trains'][i]['name'] + ' (Tr.no: ' + trainreq['trains'][i]['number'] + ')\n '
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)

		elif req['result']['parameters']['rescheduled-trains'] == 'true':
			#rescheduledTrains = req['result']['parameters']['rescheduled-trains']
			url      = 'http://api.railwayapi.com/v2/rescheduled/date/' + "{0:0=2d}".format(date.day) + '-' + "{0:0=2d}".format(date.month) + '-' + "{0:0=4d}".format(date.year) + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ")\n "
					for i in range(len(trainreq['trains'])):
						retString += str(i+1) + '. ' + trainreq['trains'][i]['name'] + '(' + trainreq['trains'][i]['number'] + ')\nRsch date: ' + trainreq['trains'][i]['rescheduled_date'] + '\nRsch time: ' + trainreq['trains'][i]['rescheduled_time'] + '\n\n'
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)

		elif req['result']['parameters']['train-route'] == 'true':
			trainName             = req['result']['parameters']['train-name']

			url      = 'http://api.railwayapi.com/v2/route/train/' + trainName + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = "(" + date.strftime("%d %B %Y") + ")\nName: " + trainreq['train']['name'] + " (" + trainreq['train']['number'] + ")" + "\nRuns on: "
					for i in range(len(trainreq['train']['days'])):
						if trainreq['train']['days'][i]['runs'] == 'Y':
							retString += trainreq['train']['days'][i]['code'] + ', '
					retString += '\nAvailable Classes: '
					for i in range(len(trainreq['train']['classes'])):
						if trainreq['train']['classes'][i]['available'] == 'Y':
							retString += trainreq['train']['classes'][i]['code'] + ', '
					retString += '\n\nRoute: \n'
					for i in range(len(trainreq['route'])):
						retString += str(i+1) + '. ' + trainreq['route'][i]['station']['name'] + '(' + trainreq['route'][i]['station']['code'] + ')\nOn day: ' + str(trainreq['route'][i]['day']) + '\nSchArr: ' + trainreq['route'][i]['scharr'] + '\nSchDep: ' + trainreq['route'][i]['schdep']  + '\n\n'

					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)

		elif req['result']['parameters']['autocomplete-station'] == 'true':
			incompleteStationName = req['result']['parameters']['incomplete-station-name']
			url      = 'http://api.railwayapi.com/v2/suggest-station/name/' + incompleteStationName.replace(' ','') + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = ""
					for i in range(len(trainreq['stations'])):
						retString += str(i+1) + '. ' + trainreq['stations'][i]['name'] + ' (' + trainreq['stations'][i]['code'] + ')\n '
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)
		
		elif req['result']['parameters']['autocomplete-train'] == 'true':
			incompleteTrainName = req['result']['parameters']['incomplete-train-name']
			url      = 'http://api.railwayapi.com/v2/suggest-train/train/' + incompleteTrainName.replace(' ','') + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if 'response_code' in trainreq:
				if try_error(trainreq['response_code']):
					retString = ""
					for i in range(len(trainreq['trains'])):
						retString += str(i+1) + '. ' + trainreq['trains'][i]['name'] + ' (' + trainreq['trains'][i]['number'] + ')\n '
					d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			return JsonResponse(d)
'''
	elif req['result']['metadata']['intentName'] == 'train_seat_availability':
		retString = 'Some error occured. Maybe try again with different phrase or sentence structure.'
		d = {
			"speech": retString,
			"displayText": retString,
			"data": {},
			"contextOut": [],
			"source": "railwaybot.pythonanywhere.com"}

		seatAvailability = req['result']['parameters']['seat-availability']
		classCode        = req['result']['parameters']['class-code']
		quotaCode        = req['result']['parameters']['quota-code']
		date             = req['result']['parameters']['date']
		trainName        = req['result']['parameters']['train-name']
		srcStation       = req['result']['parameters']['src-station']
		dstnStation      = req['result']['parameters']['dstn-station']

		if date == '':
			date = dt.datetime.strptime(req['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		elif date.split('-')[0] == 'UUUU':
			date = date.replace('UUUU', req['timestamp'].split('-')[0])
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		else:
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))

		if seatAvailability == 'true':
			url      = 'http://api.railwayapi.com/check_seat/train/' + trainName + '/source/' + srcStation + '/dest/' + dstnStation + '/date/' + "{0:0=2d}".format(date.day) + '-' + "{0:0=2d}".format(date.month) + '-' + "{0:0=4d}".format(date.year) + '/class/' + classCode.upper() + '/quota/'+ quotaCode.upper() + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			retString = "(" + date.strftime("%d %B %Y") + ")\n"
			if try_error(trainreq):
				for i in range(len(trainreq['availability'])):
					retString += str(i+1) + '. ' + trainreq['availability'][i]['date'] + ' Status: ' + trainreq['availability'][i]['status'] + '\n'


				d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			else:
				return JsonResponse(d)

	elif req['result']['metadata']['intentName'] == 'train_fare':
		retString = 'Some error occured. Maybe try again with different phrase or sentence structure.'
		d = {
			"speech": retString,
			"displayText": retString,
			"data": {},
			"contextOut": [],
			"source": "railwaybot.pythonanywhere.com"}

		trainFare   = req['result']['parameters']['train-fare']
		quotaCode   = req['result']['parameters']['quota-code']
		date        = req['result']['parameters']['date']
		trainName   = req['result']['parameters']['train-name']
		srcStation  = req['result']['parameters']['src-station']
		dstnStation = req['result']['parameters']['dstn-station']
		age         = req['result']['parameters']['age']

		if date == '':
			date = dt.datetime.strptime(req['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		elif date.split('-')[0] == 'UUUU':
			date = date.replace('UUUU', req['timestamp'].split('-')[0])
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))
		else:
			date = dt.datetime.strptime(date,"%Y-%m-%d").replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Calcutta'))

		if trainFare == 'true':
			url      = 'http://api.railwayapi.com/fare/train/' + trainName + '/source/' + srcStation.lower() + '/dest/' + dstnStation.lower() + '/age/' + age + '/quota/' + quotaCode.upper() + '/doj/' + "{0:0=2d}".format(date.day) + '-' + "{0:0=2d}".format(date.month) + '-' + "{0:0=4d}".format(date.year) + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if try_error(trainreq):
				retString = "(" + date.strftime("%d %B %Y") + ")\nFrom: " + trainreq['from']['name'] + " (" + trainreq['from']['code'] + ") To: " + trainreq['to']['name'] + " (" + trainreq['to']['code'] + ")\n"
				for i in range(len(trainreq['fare'])):
					retString += str(i+1) + '. Class: ' + trainreq['fare'][i]['code'] + ' Fare: Rs.' + trainreq['fare'][i]['fare'] + '\n'

				d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			else:
				return JsonResponse(d)

	elif req['result']['metadata']['intentName'] == 'trains_arrival':
		retString = 'Some error occured. Maybe try again with different phrase or sentence structure.'
		d = {
			"speech": retString,
			"displayText": retString,
			"data": {},
			"contextOut": [],
			"source": "railwaybot.pythonanywhere.com"}

		trainArrival = req['result']['parameters']['train-arrival']
		hour         = req['result']['parameters']['hour']
		srcStation   = req['result']['parameters']['station-name']

		if trainArrival == 'true':
			url      = 'http://api.railwayapi.com/v2/arrivals/station/' + srcStation + '/hours/' + hour + '/apikey/KEY/'
			trainreq = requests.get(url).json()

			if try_error(trainreq):
				retString = "Station code: " + trainreq["station"] + "\n"
				if trainreq['total'] != 0:
					for i in range(trainreq['total']):
						retString += str(i+1) + '. Train: ' + trainreq['train'][i]['name'] + ' (' + trainreq['train'][i]['number'] + ') \nSchArr: ' + trainreq['train'][i]['scharr'] + ' ActArr: ' + trainreq['train'][i]['actarr'] + '\nSchDep: ' + trainreq['train'][i]['schdep'] + ' ActDep: ' + trainreq['train'][i]['actdep'] + '\n\n'
				else:
					retString += 'No trains within your specified hours!'

				d['speech'] = d['displayText'] = retString
				return JsonResponse(d)
			else:
				return JsonResponse(d)
'''
