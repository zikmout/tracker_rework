from datetime import datetime
from tornado import gen
import smtplib, ssl
import tldextract
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
				'nearest_link_pos': ['http://investors.telenet.be#tcontentSRP_2011'],
				'nearest_link_neg': [], 
				'all_links_pos': ['http://phx.corporate-ir.net/External.File'], 
				'all_links_neg': [], 
				'diff_nb': 1
			  }, 
			 'result': 1
		}
		"""
		args = { k: self.get_argument(k) for k in self.request.arguments }
		print('ARGS = {}'.format(args))
		if 'fromPage' not in args:
			flash_message(self, 'danger', 'Impossible to know from what page email has to be sent.')
			self.redirect('/')
		else:
			if args['fromPage'] == 'live_view' and 'live_view' in self.session['tasks']:

				task_results = list()
				for worker in self.session['tasks']['live_view']:
					task = live_view.AsyncResult(worker['id'])
					response = get_celery_task_state(task)
					if response['state'] == 'SUCCESS' and (response['status']['diff_neg'] != []\
					 or response['status']['diff_pos'] != []):
						task_results.append(response['status'])
				#print('list of all grabbed task = {}'.format(task_results))

				html = """\
				<html>
				  <body>
				"""
				html += "<b><a name='top'>" + str(len(task_results)) + " websites have changed: </a><br> " 
				for site in task_results:
					html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

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
						if site['all_links_pos'] is None:
							pass
						elif len(site['all_links_pos']) < 10:
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
						if site['all_links_neg'] is None:
							pass
						elif len(site['all_links_neg']) < 10:
							for link in site['all_links_neg']:
								if link not in site['nearest_link_neg']:
									site_html += (link + "<br>")
						else:
							site_html += ('*** too many links ***' + "<br>")
						site_html += "</font>"
				html += site_html
				html += "<br></body></html>"

				# Turn these into plain/html MIMEText objects
				#part1 = MIMEText(text, "plain")
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
				print('DOiMAIN LIST == {}'.format(domains_list))
				print('[Live Alert Report] {}'.format(', '.join(domains_list)))
				for email in receiver_email:
                                    message = MIMEMultipart()
                                    #date = datetime.now().replace(microsecond=0)
                                    #message["Subject"] = '[{}] Alerts on share buybacks'.format(date)
                                    #message["Subject"] = '[Live Report] {}'.format(', '.join(domains_list))
                                    # Problem, subject always shows 'SBB Alert' ?!
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
