#coding:utf-8
import numpy as np 
import itchat
import PIL.Image as Image
import os
import random
from os import listdir
import matplotlib.pyplot as plt
import re
from time import sleep
from wordcloud import WordCloud, ImageColorGenerator 
import numpy as np
import pandas as pd
# from pyecharts import Map, Style, Page

def login_wechat():
	itchat.auto_login()
	friends = itchat.get_friends(update=True)
	# print("friends", friends)
	print("friends number: ", len(friends))
	return friends

def get_imgs(friends):
	for num, friend in enumerate(friends):
		print("friend", friend)
		img = itchat.get_head_img(userName=friend["UserName"])
		fileImg = open("./user/" + str(num) + ".jpg", 'wb')
		fileImg.write(img)
		fileImg.close()

def get_big_img():
	pics = listdir("user")  
	# print(pics)
	random.shuffle(pics)
	numPic = len(pics)

	tolImg = Image.new("RGB", (900, 900)) # new func

	x = 0
	y = 0

	for i in pics:
		try:
			img = Image.open("user/{}".format(i))
		except IOError:
			print("Error: Can't find file or read file failed")
		else:
			img = img.resize((60, 60), Image.ANTIALIAS)
			tolImg.paste(img, (x*60, y*60))

			x += 1
			if x == 900/60:
				x = 0
				y += 1

	tolImg.save("WechatBigImage.png")
	itchat.send_image('WechatBigImage.png', 'filehelper')
	print("Send Image successfully.")


def get_sex(friends):
	sex = dict()
	for friend in friends:
		if friend["Sex"] == 1:
			sex["man"] = sex.get("man", 0) + 1
		elif friend["Sex"] == 2:
			sex["woman"] = sex.get("woman", 0) + 1
		else:
			sex["unknown"] = sex.get("unknown", 0) + 1

	for i, key in enumerate(sex):
		plt.bar(key, sex[key])
	
	plt.savefig("sex_distribution.png")
	plt.ion()
	plt.pause(5)
	plt.close()
	print("Save gender distribution successfully")

def get_address(friends):
	nick_name  = []
	province = []
	city = []
	for i, friend in enumerate(friends):
		nick_name.append(friend["NickName"] + " - " + str(i))
		province.append(friend["Province"])
		city.append(friend["City"])
	data = {
		'NickName': nick_name,
		'Province': province,
		'City': city
	}
	df = pd.DataFrame(data)
	df.to_excel("province_city.xlsx")
	print("Save friends address susccessfully")


def generate_loc_distribution(file_name):
	df = pd.read_excel(file_name + ".xlsx")
	aggProvince = df.groupby(['Province'])['NickName'].count().reset_index()  #agg({"friends#" : np.size}).reset_index()
	aggProvince.sort_values(by=["NickName"], ascending=False, inplace=True)
	aggProvince =aggProvince[0:10]
	# print(aggProvince)
	
	plt.bar(aggProvince["Province"], aggProvince["NickName"])

	for x,y in zip(aggProvince["Province"], aggProvince["NickName"]):
		# 在(x, y+0.01)位置处显示y轴的坐标值，ha=horizontal alignment(水平对齐方式)为居中对齐，va=vertical alignment(垂直对齐)设置为底部对齐方式
		plt.text(x, y+0.01, "%d" % y, ha='center', va='bottom')


	plt.xlabel("Province")
	plt.ylabel("friends#")
	plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #显示中文标签
	
	plt.savefig("friends_loc_distribution.png")
	plt.ion()
	plt.pause(5)
	plt.close()
	print("friends location distribution successfully")

	# map_distribution = Map("中国地图")
	# chart.add('', list(aggProvince["Province"]), list(aggProvince), s_label_show=True, is_visualmap=True, visual_text_color='#000')
	# page = Page()
	# page.add(chart)











def get_signature(friends):
	file = open('sign.txt', 'w', encoding="utf-8")
	for friend in friends:
		signature = friend['Signature'].strip().replace("emoji", "").replace("span", "").replace("class", "")

		rec = re.compile("1f\d+\w*|[<>/=]")
		signature = rec.sub("", signature)
		file.write(signature + "\n")

	print("Write signature successfully.")

def create_word_cloud(file_name):
	txt = open("{}.txt".format(file_name), encoding="utf-8").read()

	# 设置词云
	# cloud_bg = np.array(Image.open("cloud_bg.jpg"))
	wc = WordCloud(
		background_color="white",
		max_words=2000,
		font_path="C:/Windows/Fonts/simsun.ttc",
		height=500,
		width=500,
		max_font_size=60,
		random_state=30,
		# mask=cloud_bg
	)
	myword = wc.generate(txt)
	# myword.recolor(color_func=ImageColorGenerator(cloud_bg))
	plt.imshow(myword)
	plt.axis("off")
	plt.ion()
	wc.to_file('sign_word_cloud.png')
	plt.pause(5)
	plt.close()
	print('Signature word cloud generated.')


# def msg_auto_reply()


def main():
	# friends = login_wechat()

	# get_imgs(friends)
	# get_big_img()

	# get_sex(friends)

	# get_signature(friends)
	# create_word_cloud('sign')

	# get_address(friends)
	generate_loc_distribution('province_city')



if __name__ == "__main__":
	main()



