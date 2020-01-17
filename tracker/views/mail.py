import os
from datetime import datetime
from tornado import gen
import html as htmlib
import smtplib, ssl
import json
import tldextract
import tornado
from tornado.escape import url_unescape as url_unescape
# from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart	
from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_celery_task_state
from tracker.workers.live.live_view_worker import live_view

class UserProjectSendMail(BaseView):
	SUPPORTED_METHOD = ['POST']
	@login_required
	@gen.coroutine
	def post(self, username, projectname):
		"""
		{
			'state': 'SUCCESS', 
			'current': 100, 
			'total': 100, 
			'status': {
				'url': 'http://investors.telenet.be/phoenix.zhtml?c=241896&p=agm-share-buy-back-program', 
				'div': 'investors.telenet.be', 
				'diff_neg': [], 
				'diff_pos': [' – Telenet Group Holding NV ... shares.'], 
				'nearest_link_pos': ['http://investors.telenet.be#tcontentSRP_2011'], DICTIONNARY
				'nearest_link_neg': [], DICTIONNARY
				'all_links_pos': ['http://phx.corporate-ir.net/External.File'], 
				'all_links_neg': [], 
				'diff_nb': 1
			  }, 
			 'result': 1
		}
		"""
		args = { k: self.get_argument(k) for k in self.request.arguments }
		print('ARGS = {}'.format(args))
		errs = json.loads(args['limitErrors'])
		print('limit errors = {}'.format(errs))
		if 'fromPage' not in args:
			flash_message(self, 'danger', 'Impossible to know from what page email has to be sent.')
			self.redirect('/')
		else:
			if args['fromPage'] == 'live_view' and 'live_view' in self.session['tasks']:

				task_results = list()
				errors = list()
				total_scanned = len(self.session['tasks']['live_view'])
				for worker in self.session['tasks']['live_view']:
					task = live_view.AsyncResult(worker['id'])
					try:
						response = get_celery_task_state(task)
						if response['state'] == 'SUCCESS' and response['status']['errors'] != {}:
							errors.append(response['status']['errors'])
						if response['state'] == 'SUCCESS' and (response['status']['diff_neg'] != []\
						 or response['status']['diff_pos'] != []):
							task_results.append(response['status'])
					except Exception as e:
						pass
						# print('Task {} does not exist anymore.'.format(worker['id']))
						# print(e)
				#print('list of all grabbed task = {}'.format(task_results))

				#print('TSA RESULTS :: {}'.format(task_results))
				html = """\
				<html>
				  <body>
				"""
				html += "<b><a name='top'>" + str(len(task_results)) + " websites have changed: </a><br> " 
				for site in task_results:
					html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

				# errors = list()
				# for site in task_results:
				# 	if site['errors'] != {}:
				# 		errors.append(site['errors'])

				
				site_html = ''
				for site in task_results:
					site_html += "<br><div align='right'><a href='#top'>top</div></a><hr><h3><a name='" + site['div'] + "'>" + site['div'] + "</a></h3>\
					<h5><a href='" + site['url'] + "' target='_blank'>" + site['url'] + "</a></h5>\
					"
					found = False
					if site['diff_pos'] != []:
						site_html += "<font color='green'><b>Added Content :</b><br>"
						if len(site['diff_pos']) < 10:
							for content in site['diff_pos']:
								for k, v in site['nearest_link_pos'].items():
									if k == content:
										site_html += ('<a style="color: green; text-decoration: underline;" href="' + site['nearest_link_pos'][k] + '">' + k + "</a><br>")
										found = True
										break;
								if not found:				
									site_html += (content + "<br>")
									found = False

						else:
							site_html += ('*** too many changes ***' + "<br>")

						# SBB LINKS POS
						# if site['sbb_links_pos'] is not None and site['sbb_links_pos'] != []:
							# site_html += "<br>SBB link(s) (if not above):<br>"
						if site['sbb_links_pos'] is None:
							pass
						elif len(site['sbb_links_pos']) < 10:
							first_time = True
							for link in site['sbb_links_pos']:	
								if link not in list(site['nearest_link_pos'].values()):
									if first_time:
										site_html += "<br>SBB link(s) (if not above):<br>"
										first_time = False
									formated_link = os.path.basename(link)
									# site_html += (str(formated_link) + "<br>")
									if '.' in formated_link:
										formated_link = os.path.splitext(str(url_unescape(formated_link)))[0]
									site_html += ('<a href="' + link + '">' + formated_link + "</a><br>")
						else:
							site_html += ('*** too many sbb links ***' + "<br>")

						
						# for nearest_link in site['nearest_link_pos']:
						# 	site_html += (nearest_link + "<br>")
						site['all_links_pos'] = [_ for _ in site['all_links_pos'].copy() if _ not in site['sbb_links_pos'] and _ not in list(site['nearest_link_pos'].values())]
						if site['all_links_pos'] is None:
							pass
						elif len(site['all_links_pos']) < 10:
							first_time = True
							# if site['all_links_pos'] != []:
								# site_html += "<br>Link(s):<br>"
							for link in site['all_links_pos']:
								if first_time:
									site_html += "<br>Link(s):<br>"
									first_time = False
								# site_html += (link + "<br>")
								if link.endswith('/'):
									formated_link = link.split('/')[-2]
								else:
									formated_link = os.path.basename(link)
									# site_html += (str(formated_link) + "<br>")
								if '.' in formated_link:
										formated_link = os.path.splitext(str(url_unescape(formated_link)))[0]
								site_html += ('<a href="' + link + '">' + formated_link + "</a><br>")
						else:
							pass
							#site_html += ('*** too many links ***' + "<br>")
						site_html += "</font>"

					found = False
					if site['diff_neg'] != []:
						site_html += "<font color='red'><b><br>Deleted Content :</b><br>"
						if len(site['diff_neg']) < 10:
							for content in site['diff_neg']:
								for k, v in site['nearest_link_neg'].items():
									if k == content:
										site_html += ('<a style="color: red; text-decoration: underline;" href="' + site['nearest_link_neg'][k] + '">' + k + "</a><br>")
										found = True
										break;
								if not found:				
									site_html += (content + "<br>")
									found = False
						else:
							site_html += ('*** too many changes ***' + "<br>")
						
						# for nearest_link in site['nearest_link_neg']:
						# 	site_html += (nearest_link + "<br>")

						
						# if site['sbb_links_neg'] is not None and site['sbb_links_neg'] != []:
							# site_html += "<br>SBB link(s) (if not above):<br>"
						if site['sbb_links_neg'] is None:
							pass
						elif len(site['sbb_links_neg']) < 10:
							# SBB LINKS NEG
							first_time = True
							for link in site['sbb_links_neg']:
								if link not in list(site['nearest_link_neg'].values()):
									if first_time:
										site_html += "<br>SBB link(s) (if not above):<br>"
										first_time = False
									formated_link = os.path.basename(link)
									# site_html += (str(formated_link) + "<br>")
									if '.' in formated_link:
										formated_link = os.path.splitext(str(url_unescape(formated_link)))[0]
									site_html += ('<a href="' + link + '">' + formated_link + "</a><br>")
						else:
							site_html += ('*** too many sbb links ***' + "<br>")

						

						site['all_links_neg'] = [_ for _ in site['all_links_neg'].copy() if _ not in site['sbb_links_neg'] and _ not in list(site['nearest_link_neg'].values())]
						if site['all_links_neg'] is None:
							pass
						elif len(site['all_links_neg']) < 10:
							# ALL LINKS NEG
							first_time = True
							# if site['all_links_neg'] != []:
								# site_html += "<br>Link(s):<br>"
							for link in site['all_links_neg']:
								if link not in list(site['nearest_link_neg'].values()):
									if first_time:
										site_html += "<br>Link(s):<br>"
										first_time = False
									if link.endswith('/'):
										formated_link = link.split('/')[-2]
									else:
										formated_link = os.path.basename(link)
									if '.' in formated_link:
										formated_link = os.path.splitext(str(url_unescape(formated_link)))[0]
									# site_html += (str(formated_link) + "<br>")
									site_html += ('<a href="' + link + '">' + formated_link + "</a><br>")

									# site_html += (link + "<br>")
						else:
							pass
							#site_html += ('*** too many links ***' + "<br>")
						site_html += "</font>"
				html += site_html
				print('ERRORS 1 : {}'.format(errors))
				print('ERRORS 2 : {}'.format(errs))
				if errors != [] or errs != {}:
					html += "<br><br><b>Errors : (" + str(len(errors) + len(errs)) + "/" + str(total_scanned) + " total scanned)</b><br>"
					if errors != []:
						for err in errors:
							for k, v in err.items():
								html += "<br>{} : {}".format(k, htmlib.escape(v))
					if errs != {}:
						for k, v in errs.items():
							html += "<br>{} : {}".format(k, htmlib.escape(v))


				html += "<br></body></html>"

				html += "<br><pre style='line-height:15.86px'><wbr>______________________________<wbr>"
				html += "This is an automated email alert tracking website change(s). If you wish to unsubscribe, contact your administrator."
				html += "<wbr>______________________________<wbr></pre>"
				html += "</body></html>"

				# Turn these into plain/html MIMEText objects
				part2 = MIMEText(html, "html")

				sender_email = "simon@electricity.ai"
				if ';' in args['email']:
					receiver_email = args['email'].split(';')
				else:
					receiver_email = args['email']
				password = 'totosecret'

				if not isinstance(receiver_email, list):
					receiver_email = [receiver_email]

				domains_list = [tldextract.extract(site['div']).domain.upper() for site in task_results]
				for email in receiver_email:
									message = MIMEMultipart()
									message["Subject"] = '[Live Alert Report] {}'.format(', '.join(domains_list))
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
				flash_message(self, 'success', 'Report successfully sent to {} .'.format(args['email']))
				self.redirect('/')
			else:
				flash_message(self, 'danger', 'There has been a problem sending mail.')
				self.redirect('/')
