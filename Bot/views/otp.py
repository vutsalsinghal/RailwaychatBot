from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import urllib.request as urllib2
import http.cookiejar as cookielib

def SMS(msg, to_number, username, passwd):
	message  = msg

	message = "+".join(message.split(' '))

	url ='http://site24.way2sms.com/Login1.action?'
	data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

	cj= cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
	try:
		usock =opener.open(url, str.encode(data))
	except IOError:
		print("error1")

	jession_id        =str(cj).split('~')[1].split(' ')[0]
	send_sms_url      = 'http://site24.way2sms.com/smstoss.action?'
	send_sms_data     = 'ssaction=ss&Token='+jession_id+'&mobile='+str(to_number)+'&message='+message+'&msgLen=136'
	opener.addheaders =[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
	try:
		sms_sent_page = opener.open(send_sms_url,str.encode(send_sms_data))
	except IOError:
		print("error2")

@csrf_exempt
def page(request):
	req = json.loads(str(request.body, 'utf-8'))

	if len(req['phoneNumber']) != 10:
		return JsonResponse({'response-code':200, 'error':'not_ten_digit'})
	else:
		SMS(req['code'],req['phoneNumber'], req['username'], req['password'])
		return JsonResponse({'response-code':200, 'error':'success'})