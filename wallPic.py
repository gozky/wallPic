# -*- coding: utf-8 -*-

import os
import sys
import requests
from bs4 import BeautifulSoup

url_home = 'http://desk.zol.com.cn'
category_url = '/fengjing/'
url = url_home+category_url

# http请求头
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'}

#get the url of each pic, then add into list_url
def get_pic_list_url(url):
	picList_url = []
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content)

	for li_tag in soup.find_all("li", class_='photo-list-padding'):
		pic_href = li_tag.a['href']
		picList_url.append(url_home+pic_href)

	return picList_url

def download_pic(url):
	picList_url = get_pic_list_url(url)

	for item in picList_url:
		pic_url = item
		while True:
			try:
				r = requests.get(pic_url, headers=headers)
			except Exception, e:
				print pic_url
				raise e
			
			soup = BeautifulSoup(r.content)
			
			wrapper_tag = soup.find_all('div', class_ = "wrapper photo-tit clearfix")
			title_tag = wrapper_tag[0].find_all('a')[0]
			seq = wrapper_tag[0].find_all('span', class_='current-num')
			file_name = title_tag.string + seq[0].string + ".jpg"
			#print file_name

			if soup.find("dd", id = "tagfbl")==None or soup.find("dd", id = "tagfbl").a.get('id') == None:
				print pic_url+'***********'
				# 该图集下下一张图片的url，下同
				next_pic_url = url_home +  soup.find("a", id = "pageNext")['href']
				# 当下一张图片的url与第一张图片的url相同时，则说明该图集已下载完，下同
				if next_pic_url== item:
					break
				pic_url = next_pic_url
				continue


			# download the most high resolution picture
			high_res_pic = soup.find('dd', id='tagfbl')
			high_res_url = url_home+ high_res_pic.a['href']

			high_res_r = requests.get(high_res_url, headers=headers)
			high_res_soup = BeautifulSoup(high_res_r.content)
			img_url = high_res_soup.find('img' )['src']
			img_r = requests.get(img_url, headers=headers)

			# create the folder 'pic'
			path = os.getcwd()
			path = os.path.join(path, 'pictures')
			if not os.path.exists(path):
				os.mkdir(path)

			filepath = os.path.join(path, file_name)

			if not os.path.exists(filepath):
				f = open(filepath, 'wb')
				print 'downloading ' + file_name+"..."
				f.write(img_r.content)
				f.close()
			else:
				break
			if (soup.find("a", id='pageNext')['href']=='javascript:;'):
				break
			else:
				next_pic_url = url_home+soup.find("a", id='pageNext')['href']
			if(next_pic_url==item):
				break
			pic_url = next_pic_url
			print pic_url
		
			
download_pic(url)
