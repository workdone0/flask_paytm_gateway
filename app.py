# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import Checksum
import requests
import os
from flask import Flask, render_template, url_for, redirect, session, escape, request


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

# initialize dictionary with request parameters
paytmParams = {

	# Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	"MID" : "#YOUR_MID",

	# Find your WEBSITE in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	"WEBSITE" : "WEBSTAGING",

	# Find your INDUSTRY_TYPE_ID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	"INDUSTRY_TYPE_ID" : "Retail",

	# WEB for website and WAP for Mobile-websites or App
	"CHANNEL_ID" : "WEB",

	# Enter your unique order id
	"ORDER_ID" : "1220",

	# unique id that belongs to your customer
	"CUST_ID" : "125",

	# customer's mobile number
	"MOBILE_NO" : "#Consumer_mob_no",

	# customer's email
	"EMAIL" : "#Consumer_email",

	# Amount in INR that is payble by customer
	# this should be numeric with optionally having two decimal points
	"TXN_AMOUNT" : "200",

	# on completion of transaction, we will send you the response on this URL
	"CALLBACK_URL" : "http://127.0.0.1:5000/pay_status",
}

# Generate checksum for parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
checksum = Checksum.generate_checksum(paytmParams, "#your_Merchant_Key")

# for Staging
url = "https://securegw-stage.paytm.in/order/process"


@app.route('/')
def index():
    return render_template('payment.html',paytmParams=paytmParams,checksum=checksum)


@app.route('/pay_status', methods=['GET','POST'])
def paystatus():
	paytmChecksum = {}
	data = {}
	if request.method == 'POST' :
		data = request.form
		
		for key, value in data.items(): 
			if key == 'CHECKSUMHASH':
				paytmChecksum = value
			else:
				paytmParams[key] = value

		isValidChecksum = Checksum.verify_checksum(paytmParams, "#YOUR_Merchant_Key", paytmChecksum)
		if isValidChecksum:
			print("Checksum Matched")
		else:
			print("Checksum Mismatched")

		return render_template("success.html",data=data)	


if __name__ == '__main__':
    app.run(debug=True)