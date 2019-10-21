# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 14:42:39 2018

@author: Ben
"""

import tkinter as tk 
import random as rand
import numpy as np

b_size = [19,19] # row,column
BLOCK_SIZE   = 24 # 每格的大小
BORDER_SIZE  = 15 # 邊界寬度
TEXT_SIZE    = 23 # 文字大小
WIDTH        = (b_size[1] - 1) * BLOCK_SIZE + BORDER_SIZE * 2 # 畫布寬度
HEIGHT = (b_size[0] - 1) * BLOCK_SIZE + BORDER_SIZE * 2 + TEXT_SIZE # 畫布高度
BG_COLOR     = "#FFDDAA" # 底色
TXT_COLOR    = "#FFFFFF" # 文字顏色
TXT_BG_COLOR = "#000000" # 文字區塊底色
WHITE_COLOR  = "#FFFFFF" # 白色
BLACK_COLOR = "#000000" # 黑色

board = np.zeros((b_size[0],b_size[1]),dtype=int) # 儲存棋盤資料
blackFlag = True # 黑子的回合
endding = False # 結束狀態

ComputerTurn = True # 電腦的回合

#tk initialize
root = tk.Tk()
root.title("五子棋") # 視窗標題
root.maxsize(width=WIDTH, height=HEIGHT) # 限制視窗大小
root.minsize(width=WIDTH, height=HEIGHT) # 限制視窗大小
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#canvas initialize
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT) # 建立畫布
canvas.place(relx=0, rely=0, anchor="nw")# 使用 place 設定畫布位置

#initialize
def drawInit():
    global blackFlag, board, endding
    blackFlag = True # 黑子先下
    endding = False # 初始化結束狀態
    board = np.zeros((b_size[0],b_size[1]),dtype=int) # 初始化棋盤資料
    
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BG_COLOR) # 棋盤區塊
    canvas.create_rectangle(0, (HEIGHT - TEXT_SIZE), WIDTH, HEIGHT, fill=TXT_BG_COLOR) # 文字區塊

    for i in range(0, b_size[0]): # 繪製格線
        canvas.create_line(BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE, WIDTH - BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE)
    for i in range(0, b_size[1]): # 繪製格線
        canvas.create_line(BORDER_SIZE + i * BLOCK_SIZE, BORDER_SIZE, BORDER_SIZE + i * BLOCK_SIZE, HEIGHT - BORDER_SIZE - TEXT_SIZE)
    #computer first
    if ComputerTurn:
        chess(rand.randint(2, b_size[0] - 3), rand.randint(2, b_size[1] - 3))
        
#show text
def drawText(message):
    canvas.create_rectangle(0, (HEIGHT - TEXT_SIZE), WIDTH, HEIGHT, fill=TXT_BG_COLOR) # 文字區塊
    canvas.create_text(5, HEIGHT - 5, fill=TXT_COLOR, text=message, anchor=tk.SW) # 顯示文字
    
#player add
def playerplay(event):
    global endding
    if endding == True: # 判斷遊戲是否結束
        drawInit() # 遊戲結束時初始化棋盤
        endding = False
    else:
        x = int((event.x - BORDER_SIZE) / BLOCK_SIZE + 0.5) # 滑鼠點擊的位置
        y = int((event.y - BORDER_SIZE) / BLOCK_SIZE + 0.5) # 滑鼠點擊的位置
        drawText('%s : add at (%s, %s)' % ("Black" if blackFlag == True else "White", x + 1, y + 1)) # 顯示下棋的位置
        r = chess(x, y) # 檢查是否已有棋子
        #computer calc
        if r == 0: # 如果沒有棋子
            c = search(1) # 計算電腦棋子連株數
            p = search(2) # 計算玩家棋子連株數
            if c[2] > p[2]: # 如果電腦連株數較高
                chess(c[0], c[1]) # 繼續增加電腦連株數
            else:
                chess(p[0], p[1]) # 否則阻擋玩家連珠
def search(flag):

    score = [0, 0, 0]
    s = 0
    for x in range(0, b_size[1]):
        for y in range(0, b_size[0]):

            s = result(x, y, flag) # 最大連株數
            if score[2] < s and board[x][y] == 0:
                score[0] = x
                score[1] = y 
                score[2] = s
    return score

#game result
def result(x, y, flag):

    assess  = [ 1, 1, 1, 1]
    posiArr = [ 1, 2, 3, 4]
    negaArr = [-1,-2,-3,-4]
    zeroArr = [ 0, 0, 0, 0]
    #row
    assess[0] += check(x, y, posiArr, zeroArr, flag) # 右連珠數
    assess[0] += check(x, y, negaArr, zeroArr, flag) # 左連珠數
    #column
    assess[1] += check(x, y, zeroArr, posiArr, flag) # 上連珠數
    assess[1] += check(x, y, zeroArr, negaArr, flag) # 下連珠數
    #upper left & under right
    assess[2] += check(x, y, negaArr, negaArr, flag) # 左下連珠數
    assess[2] += check(x, y, posiArr, posiArr, flag) # 右上連珠數
    #upper right & under keft
    assess[3] += check(x, y, negaArr, posiArr, flag) # 左上連珠數
    assess[3] += check(x, y, posiArr, negaArr, flag) # 右下連珠數
    
    return findMax(assess) # 回傳最大連株數

def findMax(arr):
    m = 0
    for i in arr:
        if i > m:
            m = i
    return m
    
def check(x, y, xRange, yRange, flag):
    count = 0
    for i in range(0, (5 - 1)):
        nx = x + xRange[i]
        ny = y + yRange[i]
        if nx >= b_size[1] or ny >= b_size[0] or nx < 0 or ny < 0:
            continue
        if board[nx][ny] == flag:
            count += 1
        elif board[nx][ny] == 0:
            count += 0.4
            break
        else:
            break
        
    return count

#Add chess
def chess(x, y):
    global blackFlag, endding, ComputerTurn
    if board[x][y] == 0: # 如果此位置是空的
        board[x][y] = 1 if blackFlag == True else 2 # 黑子的值為 1, 白子為 2
        px = BORDER_SIZE + x * BLOCK_SIZE - BLOCK_SIZE / 2 # 棋子位置
        py = BORDER_SIZE + y * BLOCK_SIZE - BLOCK_SIZE / 2 # 棋子位置
        color = BLACK_COLOR if blackFlag == True else WHITE_COLOR # 棋子顏色
        canvas.create_arc(px, py, px + BLOCK_SIZE, py + BLOCK_SIZE, start=0, extent=359, style=tk.CHORD, fill=color) # 畫出棋子
        flag = 1 if blackFlag == True else 2 # 黑子的值為 1, 白子為 2
        if result(x, y, flag) >= 5: # 如果連珠數大於等於 5 
            drawText("%s win! Please press key to replay." % ("Black" if blackFlag else "White")) # 顯示勝方
            endding = True # 遊戲結束
            ComputerTurn = (not ComputerTurn) # 下一局換對方先
        blackFlag = (not blackFlag) # 下一回合換對方
        return 0
    else:
        drawText("This location was already has chess.")
        return 1

def firstplayer():
    global ComputerTurn
    print('Please chose the first player.')
    player1 = input("'c' for computer, 'p' for player.\n") # 請求輸入先手

    if player1 == 'c': # 輸入'c'代表電腦先
        print('Computer first.')
        ComputerTurn = True
    elif player1 == 'p': # 輸入'p'代表玩家先
        print('Player first.')
        ComputerTurn = False
    else: # 輸入錯誤時重新輸入
        print('Wrong input!')
        firstplayer()
    return ComputerTurn

firstplayer() # 選擇先手       
#show initialize
drawInit() # 初始化棋盤
drawText("Initialize.") # 顯示 Initialize

#set event
canvas.focus_set()
canvas.bind("<Button-1>", playerplay) # 點擊左鍵時玩家下棋
root.mainloop()