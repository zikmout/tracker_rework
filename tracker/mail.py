import json
import html as htmlib
from datetime import datetime
import smtplib, ssl
import tldextract
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart	

# TODO: Make on function for all mails

def simple_mail_sbb(task_results, mailing_list, total_scanned):
    #print('list of all grabbed task = {}'.format(task_results))

    html = """\
    <html>
      <body>
    """
    html += "<b><a name='top'>" + str(len(task_results)) + " websites have changed: </a><br> " 
    for site in task_results:
        html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

    html += "</b><br>"

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
    # html += "<br><br>Best regards,<br>"

    # Errors logging in mail (sent to everyone yet)
    if errors != {}:
        html += "<br><br><b>Errors : (" + str(len(errors)) + "/" + str(total_scanned) + " total scanned)</b><br>"
        for k, v in errors.items():
            html += "<br>{} : {}".format(k, htmlib.escape(v))

    html += "<br><pre style='line-height:15.86px'><wbr>______________________________<wbr>"
    html += "This is an automated email alert tracking website change(s). If you wish to unsubscribe, contact your administrator."
    html += "<wbr>______________________________<wbr></pre>"
    html += "</body></html>"

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

def designed_mail_sbb(task_results, mailing_list, total_scanned):
    """
            Mailing list must be of type dict here
    """
    if not isinstance(mailing_list, dict):
        raise ValueError("Mailing List must be dict type.")

    for receiver_email, targets in mailing_list.items():
        designed_task_results = [k for k in task_results if k['url'] in targets]
        # If no change observed, no need to send mail
        if len(designed_task_results) == 0:
            continue;

        html = """\
        <html>
          <body>
        """
        html += "<b><a name='top'>" + str(len(designed_task_results)) + " websites have changed: </a><br> " 
        for site in designed_task_results:
            html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

        html += "</b><br>"

        site_html = ''
        for site in designed_task_results:
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
        html += "<br>"
        if errors != {}:
            html += "<br><b>Errors : (" + str(len(errors)) + "/" + str(total_scanned) + " total scanned)</b><br>"
            for k, v in errors.items():
                html += "<br>{} : {}".format(k, htmlib.escape(v))

        html += "<br><pre style='line-height:15.86px'><wbr>______________________________<wbr>"
        html += "This is an automated email alert tracking website change(s). If you wish to unsubscribe, contact your administrator."
        html += "<wbr>______________________________<wbr></pre>"
        html += "</body></html>"

        # Turn these into plain/html MIMEText objects
        #part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        sender_email = "simon@electricity.ai"
        password = 'totosecret'

        domains_list = [tldextract.extract(site['div']).domain.upper() for site in designed_task_results]
        print('DOMAIN LIST == {}'.format(domains_list))

        message = MIMEMultipart()
        date = datetime.now().replace(microsecond=0)
        #message["Subject"] = '[{}] Alerts on share buybacks'.format(date)
        message["Subject"] = '[{}] {}'.format('SBB Alert', ', '.join(domains_list))
        message["From"] = 'Tracker Bot'
        message["To"] = receiver_email

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        #message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print('********* Mail sent to {} (SUBJECT:{}) *********'.format(receiver_email, message["Subject"]))


def generic_mail_template(task_results, errors, mailing_list, task_name, total_scanned, show_links=True):
    """
            Mailing list must be of type dict here
    """
    print('----> ERRORS IN MAIL = {} (type : {})'.format(errors, type(errors)))
    if not isinstance(mailing_list, dict):
        raise ValueError("Mailing List must be dict type.")

    for receiver_email, targets in mailing_list.items():
        designed_task_results = [k for k in task_results if k['url'] in targets]
        # If no change observed, no need to send mail
        print('DESIGNED TASK RESULST = {}'.format(designed_task_results))
        if len(designed_task_results) == 0:
            continue;

        html = """\
        <html>
          <body>
        """
        # html += "<a style='color:#32c4d1; font-weight: 700;'' href='/'>TRACKER</a><br>"
        # html += "<b><font color='blue'>"
        # html += '(ALERT TYPE :'
        # html += task_name
        # html += ")</font></b><br>"
        html += "<b><a name='top'>" + str(len(designed_task_results)) + " websites have changed: </a><br> " 
        for site in designed_task_results:
            html += "<li><a href='#" + site['div'] + "'> " + site['div'] + "</a></li>"

        html += "<br>"

        site_html = ''
        for site in designed_task_results:
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
                if show_links and site['all_links_pos'] is not None:
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
                if show_links and site['all_links_neg'] is not None:
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
        # html += "<br><br>Best regards,<br>"

        if errors != {}:
            html += "<br><br><b>Errors : (" + str(len(errors)) + "/" + str(total_scanned) + " total scanned)</b><br>"
            for k, v in errors.items():
                html += "<br>{} : {}".format(k, htmlib.escape(v))

        html += "<br><pre style='line-height:15.86px'><wbr>______________________________<wbr>"
        html += "This is an automated email alert tracking website change(s). If you wish to unsubscribe, contact your administrator."
        html += "<wbr>______________________________<wbr></pre>"
        html += "</body></html>"
        
        # Turn these into plain/html MIMEText objects
        #part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        sender_email = "simon@electricity.ai"
        password = 'totosecret'

        domains_list = [tldextract.extract(site['div']).domain.upper() for site in designed_task_results]
        #print('DOMAIN LIST == {}'.format(domains_list))

        message = MIMEMultipart()
        date = datetime.now().replace(microsecond=0)
        #message["Subject"] = '[{}] Alerts on share buybacks'.format(date)
        message["Subject"] = '[{}] {}'.format('Diff alert', ', '.join(domains_list))
        message["From"] = 'Tracker Bot'
        message["To"] = receiver_email

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print('********* Mail sent to {} (SUBJECT:{}) *********'.format(receiver_email, message["Subject"]))
