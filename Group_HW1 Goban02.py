# -*- coding: utf-8 -*-
"""
Created on Sat May 26 21:41:04 2018

@author: Ben
"""
import numpy as np
import datetime,threading

b_size = [15,15]#r,c
b = np.zeros((b_size[0],b_size[1]),dtype=int)
np.set_printoptions(threshold=np.nan)

score = 0
score_all = np.zeros((b_size[0],b_size[1]),dtype=int)

best = [3,3]

def test1():
    
    for i in range(4):
        b[i+5,10-i]=2
    b[6,5]=1
    b[6,6]=1

def board():

    print('  ','A B C D E F G H I J K L M N O')
    for i in range(b_size[0],0,-1):
        if i >= 10:
            print(str(i),end='')
            for j in b[i-1,:]:
                if j == 0:
                    print(' .',end='')
                else:
                    print(' '+str(j),end='')
            print()
        else:
            print(' '+str(i),end='')
            for j in b[i-1,:]:
                if j == 0:
                    print(' .',end='')
                else:
                    print(' '+str(j),end='')
            print()
    
def show():

    board()
    
def playerplay():
    print('playerplay')
    alphabet = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    posi_col = input("column(Upper A to Z):")
    posi_row = int(input("row(1 to 15):"))
    
    j=0
    for i in alphabet:
        if i == posi_col:
            posi = [posi_row-1,j]            
        j+=1
        
    if b[posi[0],posi[1]] == 0:
        b[posi[0],posi[1]]=2
    else:
        print("這裡已經有棋子了!")
        playerplay()
    checkwin() 
    
def computerplay():
    print('computerplay')
    
    MinMax()
    b[best[0],best[1]] = 1
    checkwin() 
                
score_table = np.array([[50, 0,1,1,0,0],#open2
                        [50, 0,0,1,1,0],#open2
                      
                       [200, 0,1,1,0,1],
                       [200, 0,1,0,1,1],
                       [200, 1,1,0,1,0],
                       [200, 1,0,1,1,0],
                      
                      [1000, 1,1,1,0,0],#closed3
                      [5000, 0,1,1,1,0],#open3
                      [1000, 0,0,1,1,1],#closed3
                    
                      [5050, 1,1,1,1,0],#closed4
                      [5050, 1,1,1,0,1],
                      [5050, 1,1,0,1,1],
                      [5050, 1,0,1,1,1],
                      [5050, 0,1,1,1,1],#closed4            
                     
                     #[50000,0,1,1,1,1,0],#open4
                   [9999999, 1,1,1,1,1]])#5

def MinMax():

    global best
    score_max = 0

    for r in range(b_size[0]):
        for c in range(b_size[1]):
            
            if b[r,c] != 1:
                if c <= 10 and np.all(b[r,c:c+5]==[0,2,2,2,0]):#horizontal
                    score_all[r,c] += 600000 
                    score_all[r,c+4] += 600000
                    print('--',r+1,c+1,'[0,2,2,2,0]')                                  
                if c <= 10 and np.all(b[r,c:c+5]==[0,2,2,2,2]):#horizontal
                    score_all[r,c] += 6000000  
                    print('--',r+1,c+1,'[0,2,2,2,2]')                                  
                if c <= 10 and np.all(b[r,c:c+5]==[2,2,2,2,0]):#horizontal
                    score_all[r,c+4] += 6000000  
                    print('--',r+1,c+1,'[2,2,2,2,0]')
                if r <= 10 and np.all(b[r:r+5,c]==[0,2,2,2,0]):#vertical
                    score_all[r,c] += 600000 
                    score_all[r+4,c] += 600000
                    print('|',r+1,c+1,'[0,2,2,2,0]')
                if r <= 10 and np.all(b[r:r+5,c]==[0,2,2,2,2]):#vertical
                    score_all[r,c] += 6000000  
                    print('|',r+1,c+1,'[0,2,2,2,2]')    
                if r <= 10 and np.all(b[r:r+5,c]==[2,2,2,2,0]):#vertical
                    score_all[r+4,c] += 6000000  
                    print('|',r+1,c+1,'[2,2,2,2,0]')
                  
                if r <= 10 and c <= 10 and b[r,c]==0 and b[r+1,c+1]==2 and b[r+2,c+2]==2 and b[r+3,c+3]==2 and b[r+4,c+4]==0:#/
                    score_all[r,c] += 600000 
                    score_all[r+4,c+4] += 600000
                    print('/',r+1,c+1,'[0,2,2,2,0]') 
                if r <= 10 and c <= 10 and b[r,c]==0 and b[r+1,c+1]==2 and b[r+2,c+2]==2 and b[r+3,c+3]==2 and b[r+4,c+4]==2:#/
                    score_all[r,c] += 6000000
                    print('/',r+1,c+1,'[0,2,2,2,2]') 
                if r <= 10 and c <= 10 and b[r,c]==2 and b[r+1,c+1]==2 and b[r+2,c+2]==2 and b[r+3,c+3]==2 and b[r+4,c+4]==0:#/
                    score_all[r+4,c+4] += 6000000
                    print('/',r+1,c+1,'[2,2,2,2,0]') 
  
                if r <= 10 and 14-c >= 4 and b[r,14-c]==0 and b[r+1,13-c]==2 and b[r+2,12-c]==2 and b[r+3,11-c]==2 and b[r+4,10-c]==0:#\
                    score_all[r,14-c] += 600000 
                    score_all[r+4,10-c] += 600000
                    print('v',r+1,15-c,'[0,2,2,2,0]') 
                if r <= 10 and 14-c >= 4 and b[r,14-c]==0 and b[r+1,13-c]==2 and b[r+2,12-c]==2 and b[r+3,11-c]==2 and b[r+4,10-c]==2:#\
                    score_all[r,14-c] += 6000000  
                    print('v',r+1,15-c,'[0,2,2,2,2]')  
                if r <= 10 and 14-c >= 4 and b[r,14-c]==2 and b[r+1,13-c]==2 and b[r+2,12-c]==2 and b[r+3,11-c]==2 and b[r+4,10-c]==0:#\
                    score_all[r+4,10-c] += 6000000  
                    print('v',r+1,15-c,'[2,2,2,2,0]')
                    
            if b[r,c]==0 and 1 <= r and r <= 13 and 1 <= c and c <= 13:
                b[r,c] = 1
                evaluate()
                score_all[r,c]+=score
                if score_all[r,c] > score_max:
                    score_max = score_all[r,c]
                    best = [r,c]
                b[r,c] = 0
                
    return best

def evaluate():
    global score
    score=0
    
    for r in range(b_size[0]):
        for c in range(b_size[1]):
            for s in range(len(score_table)):
                if c <= 10 and np.all(b[r,c:c+5]==score_table[s,1:6]):#horizontal
                    if s == 9 and b[r,c-1]==0:
                        score += 50000
                    #print('|',r+1,c+1,score_table[s,0])
                    score += score_table[s,0]                
                if r <= 10 and np.all(b[r:r+5,c]==score_table[s,1:6]):#vertical
                    if s == 9 and b[r-1,c]==0:
                            score += 50000
                    #print('--',r+1,c+1,score_table[s,0])
                    score += score_table[s,0]
                same=0
                for i in range(5):  
                    if r <= 10 and c <= 10 and np.all(b[r+i,c+i]==score_table[s,1+i]):#/
                        same+=1
                if same == 5:
                    if r-1 >= 0 and c-1 >= 0:
                        if s == 9 and b[r-1,c-1]==0:
                            score += 50000
                    #print('/',r+1,c+1,score_table[s,0])
                    score += score_table[s,0]
                
                same=0
                for i in range(5):  
                    if r <= 10 and 14-c >= 4 and np.all(b[r+i,14-i-c]==score_table[s,1+i]):#\
                            same+=1
                if same == 5:
                    if r-1 >= 0 and c+1 <= 14:
                        if s == 9 and b[r-1,c+1]==0:
                            score += 50000
                    #print('/',r+1,c+1,score_table[s,0])
                    score += score_table[s,0]
                        
finished = False

def checkwin():
    global finished
    for r in range(b_size[0]):
        for c in range(b_size[1]):
            if b[r,c] != 0:
                if c <= 10 and b[r,c]==b[r,c+1]==b[r,c+2]==b[r,c+3]==b[r,c+4]:#horizontal
                    print('--',b[r,c],'win')
                    finished = True
                if r <= 10 and b[r,c]==b[r+1,c]==b[r+2,c]==b[r+3,c]==b[r+4,c]:#vertical
                    print('|',b[r,c],'win')
                    finished = True
                if r <= 10 and c <= 10 and b[r,c]==b[r+1,c+1]==b[r+2,c+2]==b[r+3,c+3]==b[r+4,c+4]:#/
                    print('/',b[r,c],'win')
                    finished = True
            if b[r,14-c] != 0 and r <= 10 and 14-c >= 4 and b[r,14-c]==b[r+1,13-c]==b[r+2,12-c]==b[r+3,11-c]==b[r+4,10-c]:#\
                print('v',b[r,14-c],'win')
                finished = True
            
def stop():
    global finished
    stop = input("stop?")
    if stop == 'y':
        finished = True

while finished==False:
    #test1()    
    show()

    playerplay()
    show()
    
    #print(datetime.datetime.now())
    time1 = datetime.datetime.now().second
                                 
    computerplay()
    show()

    time2 = datetime.datetime.now().second
    print('spend time : ',end='')
    if time2 - time1 >= 0:
        print(time2 - time1)
    else:
        print(60 + time2 - time1)
    stop()
