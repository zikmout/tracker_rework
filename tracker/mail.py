import os
import json
import re
import html as htmlib
from decouple import config
from datetime import datetime
import smtplib
import ssl
import tldextract
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tornado
from tornado.escape import url_unescape as url_unescape
from tracker.utils import highlight_keywords

MAX_DIFF_POS_LENGTH = 500
MAX_DIFF_NEG_LENGTH = 500
MAX_SBB_LINKS_POS_LENGTH = 100
MAX_SBB_LINKS_NEG_LENGTH = 100
MAX_ALL_LINKS_POS_LENGTH = 100
MAX_ALL_LINKS_NEG_LENGTH = 100


def generic_mail_template(task_results, errors, mailing_list, task_name, total_scanned, show_links,
                          show_diff_pos=True, show_diff_neg=True):
    """
            Mailing list must be of type dict here
    """
    print('----> ERRORS IN MAIL = {} (type : {})'.format(errors, type(errors)))
    if not isinstance(mailing_list, dict):
        raise ValueError("Mailing List must be dict type.")

    # print('TASK RESULTS ==> {}'.format(task_results))
    for receiver_email, targets in mailing_list.items():
        designed_task_results = [k for k in task_results if ((k['url'] in targets) and
                                                             (k['diff_pos'] != [] and show_diff_pos) or (k['diff_neg'] != [] and show_diff_neg))]
        # If no change observed, no need to send mail
        if len(designed_task_results) == 0:
            continue

        html = """\
        <html>
          <body>
        """
        html += "<b><a name='top'>" + str(len(designed_task_results))
        if len(designed_task_results) == 1:
            html += " website has changed (" + task_name + " alert): </a><br> "
        else:
            html += " websites have changed (" + \
                task_name + " alert): </a><br> "
        uniq_changes = list(set([_['div'] for _ in designed_task_results]))
        for site in uniq_changes:
            html += "<li><a href='#" + site + "'> " + site + "</a></li>"

        site_html = ''
        for site in designed_task_results:
            if (site['diff_pos'] != [] and show_diff_pos is True) or (site['diff_neg'] != [] and show_diff_neg is True):
                site_html += "<br><div align='right'><a href='#top'>top</div></a><hr><h3><a name='" + site['div'] + "'>" + site['div'] + "</a></h3>\
                <h5><a href='" + site['url'] + "' target='_blank'>" + site['url'] + "</a></h5>"

            if site['diff_pos'] != [] and show_diff_pos is True:
                site_html += "<font color='green'><b>Added :</b><br>"

                # DIFF POS
                if len(site['diff_pos']) < MAX_DIFF_POS_LENGTH:
                    for content in site['diff_pos']:
                        for k, v in site['nearest_link_pos'].items():
                            if k == content:
                                # print('K = {}, CONTENT = {}'.format(k, content))
                                content2 = highlight_keywords(
                                    site['keywords'], content)
                                site_html += ('<a style="color: green; text-decoration: underline;" href="' +
                                              site['nearest_link_pos'][k] + '">' + content2 + "</a><br>")
                                break

                    remainder = list(set(site['diff_pos']).difference(
                        set(list(site['nearest_link_pos'].keys()))))
                    for r in remainder:
                        content2 = highlight_keywords(site['keywords'], r)
                        site_html += (content2 + "<br>")
                else:
                    site_html += ('*** too many changes ***' + "<br>")

                # SBB LINKS POS
                if task_name == 'sbb':
                    if site['sbb_links_pos'] is None:
                        pass
                    elif len(site['sbb_links_pos']) < MAX_SBB_LINKS_POS_LENGTH:
                        first_time = True
                        for link in site['sbb_links_pos']:
                            if link not in list(site['nearest_link_pos'].values()):
                                if first_time:
                                    site_html += "<br>SBB link(s) (if not above):<br>"
                                    first_time = False
                                formated_link = os.path.basename(link)
                                if '.' in formated_link:
                                    formated_link = os.path.splitext(
                                        str(url_unescape(formated_link)))[0]
                                site_html += ('<a href="' + link +
                                              '">' + formated_link + "</a><br>")
                    else:
                        site_html += ('<BR>*** too many sbb links ***' + "<br>")

                # ALL LINKS POS
                site['all_links_pos'] = [_ for _ in site['all_links_pos'].copy(
                ) if _ not in list(site['nearest_link_pos'].values())]
                if task_name == 'sbb':
                    site['all_links_pos'] = [
                        _ for _ in site['all_links_pos'].copy() if _ not in site['sbb_links_pos']]

                if site['all_links_pos'] is None or show_links is False:
                    pass
                elif len(site['all_links_pos']) < MAX_ALL_LINKS_POS_LENGTH:
                    first_time = True
                    for link in site['all_links_pos']:
                        if first_time:
                            site_html += "<br>Link(s):<br>"
                            first_time = False
                        if link.endswith('/'):
                            formated_link = link.split('/')[-2]
                        else:
                            formated_link = os.path.basename(link)
                        if '.' in formated_link:
                            formated_link = os.path.splitext(
                                str(url_unescape(formated_link)))[0]
                        site_html += ('<a href="' + link + '">' +
                                      formated_link + "</a><br>")
                else:
                    site_html += ('<BR>*** too many links ***' + "<br>")
                site_html += "</font>"

            if site['diff_neg'] != [] and show_diff_neg is True:

                if site['diff_pos'] != [] and show_diff_pos is True:
                    site_html += "<br>"
                site_html += "<font color='red'><b>Deleted :</b><br>"

                # DIFF NEG
                if len(site['diff_neg']) < MAX_DIFF_NEG_LENGTH:
                    for content in site['diff_neg']:
                        for k, v in site['nearest_link_neg'].items():
                            if k == content:
                                content2 = highlight_keywords(
                                    site['keywords'], content)
                                site_html += ('<a style="color: red; text-decoration: underline;" href="' +
                                              site['nearest_link_neg'][k] + '">' + content2 + "</a><br>")
                                break

                    remainder = list(set(site['diff_neg']).difference(
                        set(list(site['nearest_link_neg'].keys()))))
                    for r in remainder:
                        content2 = highlight_keywords(site['keywords'], r)
                        site_html += (content2 + "<br>")

                else:
                    site_html += ('*** too many changes ***' + "<br>")

                # SBB LINKS NEG
                if task_name == 'sbb':
                    if site['sbb_links_neg'] is None:
                        pass
                    elif len(site['sbb_links_neg']) < MAX_SBB_LINKS_NEG_LENGTH:
                        first_time = True
                        for link in site['sbb_links_neg']:
                            if link not in list(site['nearest_link_neg'].values()):
                                if first_time:
                                    site_html += "<br>SBB link(s) (if not above):<br>"
                                    first_time = False
                                formated_link = os.path.basename(link)
                                if '.' in formated_link:
                                    formated_link = os.path.splitext(
                                        str(url_unescape(formated_link)))[0]
                                site_html += ('<a href="' + link +
                                              '">' + formated_link + "</a><br>")
                    else:
                        site_html += ('*** too many sbb links ***' + "<br>")

                # ALL LINKS NEG
                site['all_links_neg'] = [_ for _ in site['all_links_neg'].copy(
                ) if _ not in list(site['nearest_link_neg'].values())]
                if task_name == 'sbb':
                    site['all_links_neg'] = [
                        _ for _ in site['all_links_neg'].copy() if _ not in site['sbb_links_neg']]

                if site['all_links_neg'] is None or show_links is False:
                    pass
                elif len(site['all_links_neg']) < MAX_ALL_LINKS_NEG_LENGTH:
                    first_time = True
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
                                formated_link = os.path.splitext(
                                    str(url_unescape(formated_link)))[0]
                            site_html += ('<a href="' + link +
                                          '">' + formated_link + "</a><br>")
                else:
                    site_html += ('<BR>*** too many links ***' + "<br>")

                site_html += "</font>"

        html += site_html
        # html += "<br><br>Best regards,<br>"

        if errors != {}:
            html += "<br><br><b>Errors : (" + str(len(errors)) + \
                "/" + str(total_scanned) + " fetched)</b><br>"
            for k, v in errors.items():
                # print('ERRORRS ====> k = {}, v = {}'.format(k, v))
                html += "<br>{} : {}".format(k, htmlib.escape(v))

        html += "<br><pre style='line-height:15.86px'><wbr>______________________________<wbr>"
        html += "This is an automated email alert tracking website change(s). If you wish to unsubscribe, contact your administrator."
        html += "<wbr>______________________________<wbr></pre>"
        html += "</body></html>"

        # Turn these into plain/html MIMEText objects
        # part1 = MIMEText(text, "plain")
        part = MIMEText(html, "html")

        sender_email = config('GMAIL_SENDER_EMAIL')
        password = config('GMAIL_APP_PASSWORD')

        domains_list = [tldextract.extract(
            site['div']).domain.upper() for site in designed_task_results]
        # print('DOMAIN LIST == {}'.format(domains_list))

        message = MIMEMultipart()
        date = datetime.now().replace(microsecond=0)
        message['Subject'] = '[Alert] {}'.format(
            ', '.join(list(set(domains_list))))
        message['From'] = 'Tracker Bot'
        message['To'] = receiver_email

        message.attach(part)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print('********* Mail sent to {} (SUBJECT:{}) *********'.format(
            receiver_email, message["Subject"]))
