import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from lxml import html
from money_parser import price_str
import json

directory_list = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
url_list = []
for i in range(0,2):
	url_list.append("https://www.replacedbyrobot.info/directory/"+directory_list[i])
#print(url_list)

job_urls = []
detail = []
context = {}
with open('results.json', 'a') as fp:
	fp.write('[')
for i in range(len(url_list)):
	page_content = requests.get(url_list[i])
	#print(page_content)
	page_content_soupify = BeautifulSoup(page_content.content, 'html.parser')
	#print(page_content_soupify)
	ultags = page_content_soupify.findAll('ul', {'class': 'jobs__list'})
	#print(ultags)
	for u in ultags:
		atags = u.findAll('a')

	#Extract job urls
	for link in atags:
		job_urls.append(link['href'])
	#print(job_urls)

	for j in range(len(job_urls)):
		job_page_content = requests.get(job_urls[j])
		urlname = job_urls[j].split('/')[-1]
		name = re.sub('-', ' ', urlname)
		context['name'] = name
		job_page_content_soupify = BeautifulSoup(job_page_content.content, 'html.parser')
		result_div = job_page_content_soupify.findAll('div',{'class':'result'})
		ptags = job_page_content_soupify.findAll('b', string = re.compile(r'^#[\d+]*'))
		for p in ptags:
			context['rank'] = int(p.text[1:])
		#print(result_div)
		for r in result_div:
			chance = r.find('h2', string = re.compile(r'.*')).text.strip()
			#intro = r.find('p', {'class':'intro'}).text.strip()
			

		#print(rank)
		
		percent = re.findall(r'[0-9]\w', chance)
		try:
			context['chance_of_automation'] = int(percent[0])
		except IndexError as e:
			pass
		else:
			pass
		finally:
			pass
		
		desc = job_page_content_soupify.find('h2', string = 'Job Description').find_next('p').contents[0]
		#soup.find(text="Address:").findNext('td').contents[0]
		#print(desc)
		context['description'] = desc
		details_list = job_page_content_soupify.find('ul',{'class':'list'})
		for d in details_list.findAll('li'):
			detail.append(d.text)

		#print(detail)
		
		try:
			for det in detail:
				soc = re.findall(r'\d{2}-\d{4}', detail[0])
				context['soc'] = soc[0]
				context['mean_annual_wage'] = float(price_str(detail[1]))
				context['mean_hourly_wage'] = float(price_str(detail[2]))
				context['no_of_people'] = int(price_str(detail[3]))
		except IndexError as e:
			print('Continue')
		else:
			pass
		finally:
			pass
		
		
		#print(context)
		
		with open('results.json', 'a') as fp:
			json.dump(context, fp, indent = 4, ensure_ascii = False)
			fp.write(',')
		detail = []
	
	
with open('results.json', 'a') as fp:
	fp.write(']')
