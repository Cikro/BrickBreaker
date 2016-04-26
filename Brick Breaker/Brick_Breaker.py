########################
# Author: Nikolas Orkic
# E-Mail: norkic@mail.uoguelph.ca
#
# Last Modified: Jan. 28th 2016
#
################################

import pygame,sys,random,time
from pygame.locals import *

#Colors
BLACK=(0,0,0)
WHITE=(255,255,255)
AQUA=( 0, 255, 255)
BLUE=( 0, 0, 255)
FUCHSIA=(255, 0, 255)
GRAY=(128, 128, 128)
GREEN=( 0, 128, 0)
LIME=( 0, 255, 0)
RED=(255, 0, 0)
SILVER=(192, 192, 192)
TEAL=( 0, 128, 128)
YELLOW=(255, 255, 0)
ORANGE=(225,160,0)

TitleColors=[AQUA,BLUE,FUCHSIA,LIME,RED,YELLOW,ORANGE]
BrickColors=[BLACK,RED,ORANGE,YELLOW,GREEN,BLUE]

pygame.init()
#surface
ScreenX=800
ScreenY=600
Screen=pygame.display.set_mode((ScreenX,ScreenY))
pygame.display.set_caption('Brick Breaker')
#borders
BL=20
BR=20
BT=30
Borders=[pygame.Rect(0,0,BL,600),pygame.Rect(ScreenX-BR,0,BR,600),pygame.Rect(0,0,ScreenX,BT)]
#paddle
paddleSet=[ScreenX/2-30,ScreenY-20,60,10]
paddleInfo=paddleSet

#Ball
Ballr=5
BallInfo=[(paddleSet[0]+(paddleSet[2]/2),paddleSet[1]-Ballr),Ballr]
#Block Dimensions - 20 blocks wide, 10 blocks to half of height.
BlockX=(ScreenX-(BL+BR))/20
BlockY=(((ScreenY/2)-BT))/10

def Menu():

    Screen.fill(BLACK)
    #Choose Font
    TitleFont = pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf', 150)
    Title="Brick Breaker"
    #y= approximite width of letter
    y=40
    color1=random.choice(TitleColors)
    color2=""
    #Display title with each letter a different color
    for x in Title:
        while color1==color2:
            color1=random.choice(TitleColors)
        MenuTitle=TitleFont.render(x, True,color1)
        MenuRectObj = MenuTitle.get_rect()
        MenuRectObj.center = (120+y, 200)
        Screen.blit(MenuTitle, MenuRectObj)
        y+=40
        color2=color1
    
    PlayFont=pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf', 100)
    #Display "Play Button"
    Play=PlayFont.render("Play",True,LIME)
    PlayObj=Play.get_rect()
    PlayObj.center=(ScreenX/2,400)
    Screen.blit(Play,PlayObj)

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            mouseX=pygame.mouse.get_pos()[0]
            mouseY=pygame.mouse.get_pos()[1]
            # TL Corner "Play" [350,360] BR [450,450]
            if event.type==MOUSEBUTTONUP and ((mouseX>=350 and mouseX<=450) and (mouseY>=360 and mouseY<=450)) :
                MainGame()
        pygame.display.update()

def CreateLevel(num,Lives):
    File=open("Level "+str(num)+".txt")
    Blocks=[]
    Line=File.readline()
    while Line!="":
        Line=Line.rstrip("\n").split(" ")
        Blocks.append(Line)
        Line=File.readline()
    File.close()
    
    Bricks,paddle=DrawMainScreen(Blocks,True,Lives)
    #Display Level Number
    LevelFont=pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf', 50)
    Level=LevelFont.render("Level"+str(num),True,LIME)
    LevelObj=Level.get_rect()
    LevelObj.center=(ScreenX/2,ScreenY/2)
    Screen.blit(Level,LevelObj)
    pygame.display.update()
    #Wait 3 seconds
    time.sleep(3)
    Bricks,paddle=DrawMainScreen(Blocks,False,Lives)
    pygame.display.update()
    return Bricks,paddle
def drawBorders(Lives):
    BorderL=pygame.draw.rect(Screen,SILVER,(0,0,BL,600))
    BorderR=pygame.draw.rect(Screen,SILVER,(ScreenX-BR,0,BR,600))
    BorderT=pygame.draw.rect(Screen,SILVER,(0,0,ScreenX,BT))
    LifeFont=pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf', 35)
    Life=LifeFont.render("Lives: "+str(Lives),True,RED)
    LifeObj=Life.get_rect()
    LifeObj.center=(50,15)
    Screen.blit(Life,LifeObj)
    pygame.display.update()
def DrawMainScreen(Blocks,Update,Lives):
    #Display Level
    Screen.fill(BLACK)
    #Borders
    drawBorders(Lives)
    #paddle
    paddle=pygame.draw.rect(Screen,BLUE,(paddleSet[0],paddleSet[1],paddleSet[2],paddleSet[3]))
    paddle=pygame.Rect(paddleSet[0],paddleSet[1],paddleSet[2],paddleSet[3])
    #ball
    ball=pygame.draw.circle(Screen,WHITE,(BallInfo[0]),BallInfo[1])
    #BolckX and BlockY are Block dimensions (Line 44)
    #Block start points
    BlockCordX=0+BL
    BlockCordY=0+BT
    Bricks=[]
    #Display current level
    for x in Blocks:
        #Resets Starting X coord per row
        BlockCordX=0+BL
        for y in range(len(Blocks[0])):
            if x[y].isdigit():
                #Draws block if 'Blocks' array position contains a number
                Bricks.append([pygame.Rect((BlockCordX,BlockCordY,BlockX,BlockY)),int(x[y])])
                pygame.draw.rect(Screen,BrickColors [int(x[y])],(BlockCordX,BlockCordY,BlockX,BlockY))
                pygame.draw.rect(Screen,BLACK,(BlockCordX,BlockCordY,BlockX,BlockY),1)

                if Update:
                    pygame.display.update()
            #adds Block width to starting X coord 
            BlockCordX+= BlockX
        #adds Block hieght to starting X coord
        BlockCordY+=BlockY
        
    return Bricks,paddle

def StartLevel(Lives):
    # Degreese 30,      45,    60,     120,    135,     150
    Target=[[17.32,0],[30,0],[52,0],[52,60],[30,60],[17.32,60]]
    LineChoice=0
    #Redraw Paddle
    pygame.draw.rect(Screen,BLACK,(paddleInfo[0],paddleInfo[1],paddleInfo[2],paddleInfo[3]))
    pygame.draw.rect(Screen,BLUE,(paddleSet[0],paddleSet[1],paddleSet[2],paddleSet[3]))
    paddle=pygame.Rect(paddleSet[0],paddleSet[1],paddleSet[2],paddleSet[3])
    Line=pygame.draw.line(Screen,GRAY,(BallInfo[0]),(paddleSet[0],paddleSet[1]-Target[0][0]),2)
    ball=pygame.draw.circle(Screen,WHITE,(BallInfo[0]),BallInfo[1])
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
           #Event= Left Arrow
            if event.type==pygame.KEYDOWN:
                if event.key==K_LEFT and LineChoice!=0:
                    #cover Target Line
                    Line=pygame.draw.line(Screen,BLACK,(BallInfo[0]),(paddleSet[0]+Target[LineChoice][1],paddleSet[1]-Target[LineChoice][0]),2)
                    LineChoice-=1
                    #Draw new target line in different position
                    Line=pygame.draw.line(Screen,GRAY,(BallInfo[0]),(paddleSet[0]+Target[LineChoice][1],paddleSet[1]-Target[LineChoice][0]),2)
                    ball=pygame.draw.circle(Screen,WHITE,(BallInfo[0]),BallInfo[1])
                #Event=  Right Arrow
                if event.key==K_RIGHT and LineChoice!=5:
                    #Cover Target Line
                    Line=pygame.draw.line(Screen,BLACK,(BallInfo[0]),(paddleSet[0]+Target[LineChoice][1],paddleSet[1]-Target[LineChoice][0]),2)
                    LineChoice+=1
                    #Draw new target line in different position
                    Line=pygame.draw.line(Screen,GRAY,(BallInfo[0]),(paddleSet[0]+Target[LineChoice][1],paddleSet[1]-Target[LineChoice][0]),2)
                    ball=pygame.draw.circle(Screen,WHITE,(BallInfo[0]),BallInfo[1])

                if event.key==K_SPACE:
                    #Cover Target line
                    Line=pygame.draw.line(Screen,BLACK,(BallInfo[0]),(paddleSet[0]+Target[LineChoice][1],paddleSet[1]-Target[LineChoice][0]),2)
                    ball=pygame.draw.circle(Screen,WHITE,(BallInfo[0]),BallInfo[1])

                    BallX=BallInfo[0][0]
                    BallY=BallInfo[0][1]
                    BallX2=(paddleSet[0]+Target[LineChoice][1])
                    BallY2=(paddleSet[1]-Target[LineChoice][0])
                    #Find rate of change in X and Y values for chosen line
                    DeltaY=(BallY2-BallY)
                    DeltaX=(BallX2-BallX)

                    return BallX,BallY,DeltaY,DeltaX,paddle
            pygame.display.update()
    
def MainGame():
    level=0
    Lives=10
    global paddleInfo
    while Lives>0:
        #Create Level
        level+=1
        if level<=10:
            Bricks,paddle=CreateLevel(level,Lives)
        #If Level 10 is beaten, You won
        else:
            Screen.fill(BLACK)
            #Print "You Won" Text
            YouWinFont=pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf',100)
            YouWin=YouWinFont.render(" Congratulations, You Won",True,LIME)
            YouWinObj=YouWin.get_rect()
            YouWinObj.center=(ScreenX/2,ScreenY/2)
            Screen.blit(YouWin,YouWinObj)
            pygame.display.update()
            time.sleep(3)
            #Main Menu
            Menu()
        BallX,BallY,DeltaY,DeltaX,paddle=StartLevel(Lives)
        paddleInfo=[ScreenX/2-30,ScreenY-20,60,10]
        fpsClock = pygame.time.Clock()
        FPS=60
        LMove=False
        RMove=False
        
        LBounce=True
        RBounce=True
        TBounce=True
        PBounce=True
        #Rate of Change
        ROC=6
        #While Bricks Remain and You have lives
        while max(Bricks)[0]!=0 and Lives>0:
                #Change Ball Position
                ball=pygame.draw.circle(Screen,BLACK,(int(BallX),int(BallY)),BallInfo[1])
                BallX+=DeltaX/ROC
                BallY+=DeltaY/ROC
                ball=pygame.draw.circle(Screen,WHITE,(int(BallX),int(BallY)),BallInfo[1])
                #Paddle Collsion
                if PBounce and paddle.collidepoint(BallX,BallY+(Ballr)):
                    DeltaY=-(DeltaY)
                    LBounce=True
                    RBounc=True
                    TBounce=True
                    PBounce=False
                #Left Border Collision
                if LBounce and Borders[0].collidepoint(BallX-(Ballr),BallY):
                    DeltaX=-(DeltaX)
                    LBounce=False
                    RBounc=True
                    TBounce=True
                    PBounce=True
                #Right Border Collision
                if RBounce and Borders[1].collidepoint(BallX+(Ballr),BallY):
                    DeltaX=-(DeltaX)
                    LBounce=True
                    RBounc=False
                    TBounce=True
                    PBounce=True
                #Top Border Collision
                if TBounce and Borders[2].collidepoint(BallX,BallY-(Ballr)):
                    DeltaY=-(DeltaY)
                    LBounce=True
                    RBounc=True
                    TBounce=False
                    PBounce=True
                #Ball Passes bottom
                if BallY>ScreenY:
                    #Lose 1 Life
                    Lives-=1
                    ball=pygame.draw.circle(Screen,BLACK,(int(BallX),int(BallY)),BallInfo[1])
                    drawBorders(Lives)
                    if Lives>0:
                        #Reset Paddle position
                        BallX,BallY,DeltaY,DeltaX,paddle=StartLevel(Lives)
                        paddleInfo=[ScreenX/2-30,ScreenY-20,60,10]
                        LMove=False
                        RMove=False                 
                        LBounce=True
                        RBounce=True
                        TBounce=True
                        PBounce=True
                #Brick Collision
                for x in range (len(Bricks)):
                    if  not(Bricks[x][0]==0):
                        #If Ball hits Bottom of Brick
                        if Bricks[x][0].collidepoint(BallX,BallY-Ballr) and Bricks[x][1]>0 and DeltaY<0:
                            #Invert Direction
                            DeltaY=-(DeltaY)
                            #Subtract Brick Life
                            Bricks[x][1]-=1
                            pygame.draw.rect(Screen,BrickColors[Bricks[x][1]],(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY))
                            pygame.draw.rect(Screen,BLACK,(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY),1)
                            #If Brick Life== 0, Remove Brick rectangle
                            if Bricks[x][1]==0:
                                Bricks[x][0]=0
                            LBounce=True
                            RBounc=True
                            TBounce=True
                            PBounce=True
                        #If Ball hits Left Side of Brick
                        elif Bricks[x][0].collidepoint(BallX+Ballr,BallY) and Bricks[x][1]>0 and DeltaX>0:
                            #Invert Direction
                            DeltaX=-(DeltaX)
                            #Subtract Brick Life
                            Bricks[x][1]-=1
                            pygame.draw.rect(Screen,BrickColors[Bricks[x][1]],(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY))
                            pygame.draw.rect(Screen,BLACK,(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY),1)
                            #If Brick Life== 0, Remove Brick rectangle
                            if Bricks[x][1]==0:
                                Bricks[x][0]=0
                            LBounce=True
                            RBounc=True
                            TBounce=True
                            PBounce=True
                        #If Ball hits Right Side of Brick
                        elif Bricks[x][0].collidepoint(BallX-Ballr,BallY) and Bricks[x][1]>0 and DeltaX<0:
                            #Invert Direction
                            DeltaX=-(DeltaX)
                            #Subtract Brick Life
                            Bricks[x][1]-=1
                            pygame.draw.rect(Screen,BrickColors[Bricks[x][1]],(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY))
                            pygame.draw.rect(Screen,BLACK,(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY),1)
                            #If Brick Life== 0, Remove Brick rectangle
                            if Bricks[x][1]==0:
                                Bricks[x][0]=0
                            LBounce=True
                            RBounc=True
                            TBounce=True
                            PBounce=True
                        #If Ball hits Top of Brick
                        elif Bricks[x][0].collidepoint(BallX,BallY+Ballr) and Bricks[x][1]>0 and DeltaY>0:
                            #Invert Direction
                            DeltaY=-(DeltaY)
                            #Subtract Brick Life
                            Bricks[x][1]-=1
                            pygame.draw.rect(Screen,BrickColors[Bricks[x][1]],(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY))
                            pygame.draw.rect(Screen,BLACK,(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY),1)
                            #If Brick Life== 0, Remove Brick rectangle
                            if Bricks[x][1]==0:
                                Bricks[x][0]=0
                            LBounce=True
                            RBounc=True
                            TBounce=True
                            PBounce=True
                #Move Left
                if LMove:
                    if paddleInfo[0]>=BL+1:    
                        pygame.draw.rect(Screen,BLACK,(paddleInfo[0],paddleInfo[1],paddleInfo[2],paddleInfo[3]))
                        paddleInfo[0]-=10
                #Move Right
                elif RMove:
                    if paddleInfo[0]+paddleInfo[2]<=(ScreenX-BR)-1:    
                        pygame.draw.rect(Screen,BLACK,(paddleInfo[0],paddleInfo[1],paddleInfo[2],paddleInfo[3]))
                        paddleInfo[0]+=10
                

                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
                   #Event= Left Arrow
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_LEFT:
                            LMove=True
                    elif event.type==pygame.KEYUP:
                        if event.key==K_LEFT:
                            LMove=False
                    #Event=  Right Arrow
                    if event.type==pygame.KEYDOWN:
                        if event.key==K_RIGHT:
                            RMove=True
                    elif event.type==pygame.KEYUP:
                        if event.key==K_RIGHT:
                            RMove=False
                #Redraw remaining bricks
                for x in range (len(Bricks)):
                    if Bricks[x][0]!=0:
                        pygame.draw.rect(Screen,BrickColors[Bricks[x][1]],(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY))
                        pygame.draw.rect(Screen,BLACK,(Bricks[x][0].left,Bricks[x][0].top,BlockX,BlockY),1)
                #Draw Paddle
                pygame.draw.rect(Screen,BLUE,(paddleInfo[0],paddleInfo[1],paddleInfo[2],paddleInfo[3]))
                paddle=pygame.Rect(paddleInfo[0],paddleInfo[1],paddleInfo[2],paddleInfo[3])
                #Draw Borders
                drawBorders(Lives)
                pygame.display.update()
                fpsClock.tick(FPS)
    #If you lose Print "Game Over"
    Screen.fill(BLACK)
    GameOverFont=pygame.font.Font('C:\\Windows\\Fonts\\playbill.ttf',150)
    GameOver=GameOverFont.render("Game Over",True,RED)
    GameOverObj=GameOver.get_rect()
    GameOverObj.center=(ScreenX/2,ScreenY/2)
    Screen.blit(GameOver,GameOverObj)
    pygame.display.update()
    time.sleep(3)
    #Main Menu
    Menu()
    



    
#Game
Menu()


