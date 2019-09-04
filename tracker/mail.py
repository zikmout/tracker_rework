from datetime import datetime
import smtplib, ssl
import tldextract
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart	


def mail_sbb(task_results, mailing_list):
	print('list of all grabbed task = {}'.format(task_results))

	html = """\
	<html>
	  <body>
	    <p>Hello,<br><br>
	       This is an automated email regarding alerts on share buybacks.</p>
	"""
	html += "<b><a name='top'>" + str(len(task_results)) + " websites have changed: </a><br> " 
	for site in task_results:
		html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

	html += "Please see logs below.</b><br>"

	site_html = ''
	for site in task_results:
		site_html += "<br><div align='right'><a href='#top'>top</div></a><hr><h3><a name='" + site['div'] + "'>" + site['div'] + "</a></h3>\
		<h5><a href='" + site['url'] + "' target='_blank'>" + site['url'] + "</a></h5>\
		"
		if site['diff_pos'] != []:
			site_html += "<font color='green'><b>Added Content :</b><br>"
			if len(site['diff_pos']) < 10:
				for content in site['diff_pos']:
					site_html += (content + "<br>")
			else:
				site_html += ('*** too many changes ***' + "<br>")
			if site['nearest_link_pos'] != [] or site['all_links_pos'] != []:
				site_html += "<br>Link(s):<br>"
			for nearest_link in site['nearest_link_pos']:
				site_html += (nearest_link + "<br>")
			if len(site['all_links_pos']) < 10:
				for link in site['all_links_pos']:
					if link not in site['nearest_link_pos']:
						site_html += (link + "<br>")
			else:
				site_html += ('*** too many links ***' + "<br>")
			site_html += "</font>"

		if site['diff_neg'] != []:
			site_html += "<font color='red'><b><br>Deleted Content :</b><br>"
			if len(site['diff_neg']) < 10:
				for content in site['diff_neg']:
					site_html += (content + "<br>")
			else:
				site_html += ('*** too many changes ***' + "<br>")
			if site['nearest_link_neg'] != [] or site['all_links_neg'] != []:
				site_html += "<br>Link(s):<br>"
			for nearest_link in site['nearest_link_neg']:
				site_html += (nearest_link + "<br>")
			if len(site['all_links_neg']) < 10:
				for link in site['all_links_neg']:
					if link not in site['nearest_link_neg']:
						site_html += (link + "<br>")
			else:
				site_html += ('*** too many links ***' + "<br>")
			site_html += "</font>"
	html += site_html
	html += "<br><br>Best regards,<br></body></html>"

	# Turn these into plain/html MIMEText objects
	#part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")

	sender_email = "simon@electricity.ai"
	if ';' in mailing_list:
		receiver_email = mailing_list.split(';')
	else:
		receiver_email = mailing_list
	password = 'totosecret'

	if not isinstance(receiver_email, list):
		receiver_email = [receiver_email]

	domains_list = [tldextract.extract(site['div']).domain.upper() for site in task_results]
	print('DOMAIN LIST == {}'.format(domains_list))
	for email in receiver_email:
		message = MIMEMultipart()
		date = datetime.now().replace(microsecond=0)
		#message["Subject"] = '[{}] Alerts on share buybacks'.format(date)
		message["Subject"] = '[SBB Alert] {}'.format(', '.join(domains_list))
		message["From"] = 'Tracker Bot'
		message["To"] = email

		# Add HTML/plain-text parts to MIMEMultipart message
		# The email client will try to render the last part first
		#message.attach(part1)
		message.attach(part2)

		# Create secure connection with server and send email
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		    server.login(sender_email, password)
		    server.sendmail(
		        sender_email, email, message.as_string()
		    )
	print('********* ALL MAILS SENT !! *****')