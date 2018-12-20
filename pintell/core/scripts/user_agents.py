import os
import requests as req
from bs4 import BeautifulSoup
import time

# script highly inspired from https://github.com/tamimibrahim17/List-of-user-agents

def save_direct_loadable_list(filename, user_agent_list):
	fd = open(os.path.join(os.getcwd(), filename + '.py'), 'w+')
	fd.write('USER_AGENTS = [\n')
	l = len(user_agent_list)
	idx = 0
	for _ in user_agent_list:
		idx += 1
		if idx != l:
			fd.write('\'' + _ + '\',\n')
		else:
			fd.write('\'' + _ + '\']\n')
	fd.close()

def save(br,ua):

	file = os.path.join(os.getcwd(), br +'.txt')
	print('file_path = {}'.format(file))
	with open(file,'w+') as f:
		for user_agent in ua:
			f.write(user_agent + '\n')

def getUa(br):

	url = 'http://www.useragentstring.com/pages/useragentstring.php?name='+br
	r = req.get(url)

	print('Trying to get User-Agents for url {}\n'.format(url))

	if r.status_code == 200:
		soup = BeautifulSoup(r.content,'html.parser')
	else:
		soup = False

	if soup:
		div = soup.find('div',{'id':'liste'})
		lnk = div.findAll('a')

		user_agent_list = list()
		for i in lnk:
			#print('i.text = {}'.format(i.text))
			if '-->>' not in i.text and 'User-Agent:' not in i.text and len(i.text) > 30 and len(i.text) < 150:
				user_agent_list.append(i.text.strip())

		try:
			#print('User-Agents list === {}'.format(user_agent_list))
			#time.sleep(5)
			user_agent_list = list(set(user_agent_list))
			save(br, user_agent_list)
		except Exception as e:
			print('Saving User-Agents for browser {} failed.\n'.format(br))
			print(e)
	else:
		print('No soup for {}'.format(br))
	return user_agent_list

all_ua = list()
lst = ['Firefox','Internet+Explorer','Opera','Safari','Chrome','Edge','Android+Webkit+Browser']

for i in lst:
	tmp = set(getUa(i))
	[all_ua.append(x) for x in tmp]

save_direct_loadable_list('user_agent_list', all_ua)
#print(set(all_ua))
print('-> Number of loaded User-Agents = {}\n'.format(len(all_ua)))
#time.sleep(20)