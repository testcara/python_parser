#!/usr/local/bin/python3
# _*_ coding: UTF-8 _*_
"""
  The module is used to parser the http://www.luoo.net/ web
  to download the musics
"""

import os
import requests
# bs4 module is used to parser the html and get the content
from bs4 import BeautifulSoup


web_url = "http://www.luoo.net/music"
music_url = "http://mp3-cdn2.luoo.net/low/luoo/radio{}/{}.mp3"

class LuooSpider():
	def __init__(self):
		self.class_urls = []
		self.class_music = {}
		self.class_music_name =[]

	def get_music_class_urls(self):
		main_page_response = requests.get(web_url)
		main_page_soup = BeautifulSoup(main_page_response.content, "html.parser")
		class_wrapper_html = main_page_soup.findChildren("div", attrs={'class':'pagenav-wrapper'})[0]
		class_wrapper_list = str(class_wrapper_html).split('</a>')
		for class_item in class_wrapper_list[:-1]:
			class_page_index = class_item.split("href=")[1].split(">")[0].replace('"', '')
			self.class_urls.append(class_page_index)


	def get_musics_songs_urls_of_classes(self):
		for class_music_url in self.class_urls:
			class_music_name = class_music_url.split('/')[-1]
			class_music_vol_url_list = []
			class_music_respone = requests.get(class_music_url)
			class_music_soup = BeautifulSoup(class_music_respone.content, 'html.parser')
			class_music_html = class_music_soup.find_all("a", attrs={'class':'name'})
			for i in class_music_html:
				class_music_vol = str(i).split('vol.')[1].split(' ')[0]
				#for song_number in ["03", "04"]:
				for song_number in ["03"]:
					class_music_vol_url = music_url.format(class_music_vol, song_number)
					class_music_vol_url_list.append(class_music_vol_url)
			self.class_music[class_music_name]=class_music_vol_url_list

	def download_songs_locally(self):
		song_number = 0
		for music_type in self.class_music:
			print("Checking urls for {}:".format(music_type))
			local_class_music_dir= "/home/music/"+ music_type
			print(local_class_music_dir)
			if not os.path.exists(local_class_music_dir):
				print("Creating music dir for {}".format(music_type))
				os.makedirs(local_class_music_dir.format(music_type))
			else:
				print("dir {} for {} music has been created".format(local_class_music_dir, music_type))
			for song in self.class_music[music_type]:
				print(song)
				song_name = song.split('radio')[1].split('/')[0]
				local_file = local_class_music_dir +  "/" + song_name + ".mp3"
				print("{}, {}".format(song_name, local_file))
				song_number += 1

				if not os.path.isfile(local_file):
					print("downloading the {} songs to {}".format(song_number, local_file))
					res = requests.get(song)
					with open(local_file, 'wb') as f:
						f.write(res.content)
						f.close()


spider = LuooSpider()
spider.get_music_class_urls()
spider.get_musics_songs_urls_of_classes()
spider.download_songs_locally()