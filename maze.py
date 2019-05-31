import requests
import json
# -*- coding: utf-8 -*-


url = 'http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com' # server url
uid = '604929653' # your uid
resp = requests.post(url + '/session', data = {'uid':uid}) # start new session
body = resp.json()
print(body)
access_token = body['token'] # retrieve access token from response body

resp = requests.get(url + '/game?token=' + access_token) # get maze information
body = resp.json()
print(body)
starting_location = body['cur_loc']

w, h = body['size'][0], body['size'][1]
Matrix = [[0 for x in range(h)] for y in range(w)] 
Matrix[starting_location[0]][starting_location[1]] = 6

# 0 means undiscovered
# 1 means discovered from left (move left to retrace)
# 2 means discovered from right (move right to retrace)
# 3 means discovered from up    (move up to retrace)
# 4 means discovered from down (move down to retrace)
# 5 means obstacle
# 6 means origin
#0,0 is top left coordinate
def checksurroundings(xpos,ypos): #true if one of the surrounding four values is a 0
	if(xpos > 0 and Matrix[xpos-1][ypos] == 0):
		return 1
	if(ypos > 0 and Matrix[xpos][ypos-1] == 0):
		return 1
	if(xpos < w-1 and Matrix[xpos+1][ypos] == 0):
		return 1
	if(ypos < h-1 and Matrix[xpos][ypos+1] == 0):
		return 1
	return 0
def backtrack(xpos, ypos):
	#print("BACKTRACKING")
	"""resp = requests.get(url + '/game?token=' + access_token) # get maze information
	body = resp.json()

	xpos = body['cur_loc'][0]
	ypos = body['cur_loc'][1]"""
	if(checksurroundings(xpos,ypos) == 1):
		return
	else:
		if(Matrix[xpos][ypos] == 1): #move left
			resp = requests.post(url + '/game?token=' + access_token, data = {'action':'left'})
			body = resp.json()
			#print(body)
			xpos-=1
			backtrack(xpos,ypos)
		elif(Matrix[xpos][ypos] == 2): #move right
			resp = requests.post(url + '/game?token=' + access_token, data = {'action':'right'})
			body = resp.json()
			#print(body)
			xpos+=1
			backtrack(xpos,ypos)
		elif(Matrix[xpos][ypos] == 3): #move up
			resp = requests.post(url + '/game?token=' + access_token, data = {'action':'up'})
			body = resp.json()
			#print(body)
			ypos-=1
			backtrack(xpos,ypos)
		elif(Matrix[xpos][ypos] == 4): #move down
			resp = requests.post(url + '/game?token=' + access_token, data = {'action':'down'})
			body = resp.json()
			#print(body)			
			ypos+=1
			backtrack(xpos,ypos)
	return
def move(xpos, ypos):
	#print(Matrix)


	if(checksurroundings(xpos,ypos) == 0):
		backtrack(xpos,ypos)
		resp = requests.get(url + '/game?token=' + access_token) # get maze information
		body = resp.json()
		xpos = body['cur_loc'][0]
		ypos = body['cur_loc'][1]
	if(xpos < w-1 and Matrix[xpos+1][ypos] == 0):
		#move right mark discovered from left if valid else mark 5
		resp = requests.post(url + '/game?token=' + access_token, data = {'action':'right'})
		body = resp.json()
		if(body['result'] == 0):
			xpos+=1
			Matrix[xpos][ypos] = 1
			move(xpos,ypos)
		if(body['result'] == -1):
			Matrix[xpos+1][ypos] = 5
		if(body['result'] == 1):
			exit()
			return 1
		if(body['result'] == -2):
			print("out of bounds! right")
			return -1
		#print("result" + str(body['result']))
		move(xpos,ypos)
	elif(ypos != h-1 and Matrix[xpos][ypos+1] == 0):
		#move down mark discovered from top
		resp = requests.post(url + '/game?token=' + access_token, data = {'action':'down'})
		body = resp.json()
		if(body['result'] == 0):
			ypos+=1
			Matrix[xpos][ypos] = 3
		if(body['result'] == -1):
			Matrix[xpos][ypos+1] = 5
		if(body['result'] == 1):
			exit()
			return 1
		if(body['result'] == -2):
			print("out of bounds! down")
			return -1
		#print("result" + str(body['result']))
		move(xpos,ypos)
	elif(xpos != 0 and Matrix[xpos-1][ypos] == 0):
		#move left mark discovered from right
		resp = requests.post(url + '/game?token=' + access_token, data = {'action':'left'})
		body = resp.json()
		if(body['result'] == 0):
			xpos-=1
			Matrix[xpos][ypos] = 2
		if(body['result'] == -1):
			Matrix[xpos-1][ypos] = 5
		if(body['result'] == 1):
			exit()			
			return 1
		if(body['result'] == -2):
			print("out of bounds! left")
			return -1
		#print("result" + str(body['result']))
		move(xpos,ypos)
	elif(ypos != 0 and Matrix[xpos][ypos-1] == 0):
		#move up 
		resp = requests.post(url + '/game?token=' + access_token, data = {'action':'up'})
		body = resp.json()
		if(body['result'] == 0):
			ypos-=1
			Matrix[xpos][ypos] = 4
		if(body['result'] == -1):
			Matrix[xpos][ypos-1] = 5
		if(body['result'] == 1):
			exit()
			return 1
		if(body['result'] == -2):
			#print("out of bounds! up")
			return -1
		#print("result" + str(body['result']))
		move(xpos,ypos)
	return 0
returnval = 0
for i in range(5):      # run five times
	returnval = 0	# want to run until we get a 1 which means we found exit
	xpos = starting_location[0]
	ypos = starting_location[1]
	returnval = move(xpos,ypos)
	#means we finished one round of stuff
resp = requests.get(url + '/game?token=' + access_token) # get maze information
body = resp.json()
#print(body)
#print(str(xpos) + "," + str(ypos))