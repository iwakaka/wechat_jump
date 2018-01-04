# -*- coding:utf-8 -*-  
import argparse
import imutils
import numpy as np
import time
import os
import sys
import cv2
import math
import random

start_time = time.time();
def printImg(img):
	cv2.imshow("Image", img)
	cv2.waitKey(0)
def writeImg(name,img):
	cv2.imwrite("C:\\Users\\longfish\\Desktop\\bbb\\"+name+".png", img)


''' 色差计算
'''
def rgbComp(r1,g1,b1,r2,g2,b2,allowance) :
	cs = 0
	#print('exception: r1,g1,b1,r2,g2,b2,allowance:  ',r1,g1,b1,r2,g2,b2,allowance)
	try:
		cs =math.sqrt((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)
	except Exception as e:
		print('exception: r1,g1,b1,r2,g2,b2,allowance:  ',r1,g1,b1,r2,g2,b2,allowance)
		raise e
	
		
	
	#print 'cs:',cs
	if cs >= allowance :
		return True
	return False

def findMe2(img):
	global w,h
	pix = img
	sum_x =0
	sum_count =0
	me_x = 0
	me_y = 0
	border = w
	left = 0
	top = int(h/3)
	for x in xrange(int(h-h/3),top,-5):
		if x < top :
			break
		for y in range(int(w/5),w):
			if y < left or y > border :
				continue
			#print(x,y)
			if y < (int(w/4) +2) :
				#print(y,int(w/4) +2)
				cv2.circle(img, (y, x), 2, (0, 0, 255), -1)
				#printImg(img)
			down_pix= pix[x,y]
			#print("--------------")
			if 50 < down_pix[2] <60 and 50 < down_pix[1] <60 and 90 < down_pix[0] <100:
				sum_x += y
				sum_count +=1
				me_y = max(me_y, x)
				#print(111111)
				cv2.circle(img, (y, x), 2, (0, 111, 255), -1)

				top = x - int(h/15)
				border = y + int(w/15)
				left = y - int(w/15)

				continue
			#print(y)
		#print("x * y:",x*y)
	if all([sum_count,sum_x]) :
		me_x = int(sum_x / sum_count)
	
	cv2.circle(img, (me_x, me_y-10), 2, (0, 255, 255), -1)
	return me_x,me_y
	

def findDist(img):
	global w,h
	#top_pix = img[h/3,1]
	
	#自己的坐标me_x,me_y
	me_x,me_y = findMe2(img)
	
	#边界点
	border_x = border_y = 0

	#print 'me_x:',me_x ,'me_y:',me_y
	center_x = center_y=0
	
	#目标物 边界横向坐标
	old_border=border =0
	
	check_count =2
	check =0
	allowance =10
	#标记扫描目标物 最上点，最上点与中心店同轴
	first_top=True
	#是否左边开始扫描 默认是
	isleft=True 
	sum_top=0
	sum_c=0
	#扫描每行像素点 根据自己(棋子)的坐标判断
	#棋子 在屏幕左半部分就从右边开始扫描每行像素点，反之从左边开始扫描
	#循环参数：start 开始横坐标，end 结束横坐标,step 扫描步长
	if me_x < w/2 :
		start = w - 1#w/16 	#从屏幕右边 出开始向左边扫描  减少循环次数
		end = w - w * 4 /7 	# 扫描至屏幕中间多一点	减少循环次数
		step = -2
		isleft = False
	else :
		start = 1#w/16
		end = w * 4 /7
		step = 2
		old_border=border =w
		
	#扫描目标物中心点
	#从h/3开始，2/3 处结束,步长为3个像素点（只扫描屏幕中间1/3）
	
	for x in xrange(h/3,me_y,2):
		first_pix = img[x,1] #每行像素的参考基点（背景点）
		first_border=True

		for y in xrange(start,end,step):
			tmp_pix = img[x,y]
			#cv2.circle(img, (y, x), 1, (0, 255, 0), -1)
			#当前点 与参考点 比较RGB值
			if rgbComp(int(first_pix[2]),int(first_pix[1]),int(first_pix[0]),\
						int(tmp_pix[2]),int(tmp_pix[1]),int(tmp_pix[0]),allowance) :
			
				if first_top :
					
					#记录最上点
					top_pix = img[x+step,y+step]
					
					sum_top +=y
					sum_c +=1
				
				if first_border:
					first_border = False
					old_border = border

					if rgbComp(int(first_pix[2]),int(first_pix[1]),int(first_pix[0]),\
						int(tmp_pix[2]),int(tmp_pix[1]),int(tmp_pix[0]),allowance):
					
						if isleft :
							border = min(border,y)
						else :
							border = max(border,y)
							#print 'max you border:',border
						border_y = x
						if border == old_border :
							check +=1
						#print 'isleft:',isleft
		cv2.circle(img, (1,x), 1, (0, 0, 255), -1)
		if sum_c > 0 and first_top :
			first_top = False
			center_x = int(sum_top/sum_c)
		if check >= check_count:
			break
	center_y = abs(border_y - check_count * 2)
	cv2.circle(img, (center_x,center_y ), 1, (0, 255, 0), -1)
	

	return me_x,me_y,center_x,center_y

def jump(dest):
	m = 0.7 #按压时间与距离 系数
	press_time = int(dest / m)
	if israndom :
		press_time = press_time + random.uniform(1, 22)
	cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {press_time}'.format(
        x1=btn_x1,
        y1=btn_y1,
        x2=btn_x1,
        y2=btn_y1,
        press_time=int(press_time))
	print 'cmd:',cmd
	os.system(cmd)
	return press_time

def getscreencap() :
	os.system('adb shell screencap -p /sdcard/autojump.png')
	os.system('adb pull /sdcard/autojump.png .')

#屏幕按压点
btn_x1 = 33
btn_y1 = 333
btn_x1 = 33
btn_y1 = 333
h=w = 0
dirpath = ''
#跳的太准了加入随机,默认不加,为 False
israndom = False

def main():
	global w,h
	
	while True:
		this_time=time.time()
		getscreencap()
		img = cv2.imread('autojump.png')
		h,w,temp = img.shape
		pix = img.copy()
		
		me_x,me_y,center_x,center_y = findDist(pix)
		if not all((me_x,me_y)) :
			break
		#writeImg("temp",img)

		jump(math.sqrt((me_x-center_x)**2+(me_y-center_y)**2))
		
		print 'me_x,me_y:(',me_x,me_y,')', 'c_x,c_y:',center_x,center_y

		print 'distance:',math.sqrt((me_x-center_x)**2+(me_y-center_y)**2)
		
		print('this time:',time.time() - this_time)
		print('run total time:' ,time.time() - start_time)

		#writeImg("temp2",img)
		time.sleep(2)
		
	
if __name__ == "__main__":
    main()

   


