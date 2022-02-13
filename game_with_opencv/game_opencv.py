import numpy as np
import cv2
import random

score = 0

def move(x , y , action):
    if action == 115 and x != 460:
        x += 10
    if action == 119 and x != 0:
        x -= 10
    if action == 100 and y != 460:
        y += 10
    if action == 97 and y != 0:
        y -= 10
    return (x,y)

def read_img(player,gan,block):
   player = cv2.imread(player)
   player = cv2.rotate(player, cv2.cv2.ROTATE_180)
   gan = cv2.imread(gan)
   (h, w) = gan.shape[:2]
   (cX, cY) = (w // 2, h // 2)
   M = cv2.getRotationMatrix2D((cX, cY), -135, 1.0)
   gan = cv2.warpAffine(gan, M, (w, h))
   block = cv2.imread(block)
   return player, gan , block

def preprocessing_image(pl_img,ga_img,bl_img):
    input = [pl_img,ga_img,bl_img]
    result = []
    for i in range(3):
        result.append(cv2.cvtColor(input[i], cv2.COLOR_BGR2GRAY))
        _ , result[i] = cv2.threshold(result[i], 1, 255, cv2.THRESH_BINARY) 
    return result

class Gan():
    global gan_pos
    def __init__(self ,x,y):
        self.x = x + 16//2
        self.y = y + 16//2
        
    def draw(self,img,arr,i):
        global ga_img_ , ga_img
        try:
            if self.y <= img.shape[0] :
                self.x += 1
                # img = cv2.rectangle(img, (self.x,self.y),(self.x+20,self.y+20) , (0, 0, 255),-1)
                roi = img[self.x:self.x+16,self.y:self.y+16]
                roi[np.where(ga_img_)] = 0
                roi += ga_img
            else :
                try:
                    arr.remove(i)
                except:
                    pass
        except:
            try:
                arr.remove(i)
            except:
                pass
        return img 
    
    def loc(self):
        return (self.x,self.y)

class block():
    def __init__(self,img):
        self.x = img.shape[1]-24
        self.y = random.randint(0,img.shape[1])
        self.speed = 10
        self.cont = 0

    def draw(self,img,arr,i):
        global score ,bl_img_,bl_img
        try:
            if self.cont == self.speed:
                self.cont = 0
                if self.y >= 0 :
                    self.x -= 1
                    # img = cv2.rectangle(img, (self.x,self.y),(self.x+20,self.y-20) , (255, 255, 255),-1)
                    roi = img[self.x:self.x+24,self.y:self.y+24]
                    roi[np.where(bl_img_)] = 0
                    roi += bl_img
                else :
                    if score != 0:
                        score -= 1
                    arr.remove(i)
                    print(score)
                    
            else:
                # img = cv2.rectangle(img, (self.x,self.y),(self.x+20,self.y-20) , (255, 255, 255),-1)
                roi = img[self.x:self.x+24,self.y:self.y+24]
                roi[np.where(bl_img_)] = 0
                roi += bl_img
                self.cont += 1
        except Exception as e:
            if score != 0:
                score -= 1
            arr.remove(i)
            print(score)
        return img

    def kill_box(self,arr,px,py,i):
        global score 
        if (px >= self.x-24 or px >= self.x+24  )and (py >= self.y -24 or py >= self.y+24) and (px <= self.x + 24 or  px <= self.x - 24 )and (py <= self.y + 24 or py <= self.y -24):
            score += 1
            arr.remove(i)
            print(score)

class game():
    def __init__(self,image):
        self.win = cv2.imread(image)
        self.arr = []
        self.arr2 = []
        self.speed = 100
        self.cont = 0

    def run(self):
        while 1:
            cv2.imshow('game_window',self.win)
            k = cv2.waitKey(1)
            player.posX , player.posY = move(player.posX , player.posY,k)
            self.win = player.draw(self.win)
            if k != -1:
            #   print(k)
                pass
            if k == 13:
                break
            if k == 32:
                x= Gan(player.posX , player.posY)
                self.arr.append(x)
                x = block(self.win)
                self.arr2.append(x)
            if self.cont == self.speed or self.speed <= 0 :
                self.cont = 0
                x = block(self.win)
                self.arr2.append(x)

            self.cont += 1
            xy = []

            for i in self.arr:
                        i.draw(self.win,self.arr,i)
                        xy.append(i.loc())
            for i in self.arr2:
                self.win = i.draw(self.win,self.arr2,i)
                i.kill_box(self.arr2,player.posX,player.posY,i)
                try:
                    for j in xy:
                        i.kill_box(self.arr2,j[0],j[1],i)
                except:
                    pass      

class player():
    def __init__(self,name,x,y):
        self.name = name
        self.posX = x
        self.posY = y
        self.imgp = [None , 1]
        self.score = 0
    
    def draw(self,img):
        global pl_img , pl_img_
        try:
            if(self.imgp[1]):
                self.imgp[0] = img.copy()
                self.imgp[1] = 0
                # img = cv2.rectangle(img, (self.posX,self.posY),(self.posX+20,self.posY+20) , (255, 255, 0),-1)
                # output = cv2.addWeighted(img[self.posX:self.posX+32,self.posY:self.posY+32],1, pl_img, 0.6,0) 
                roi = img[self.posX:self.posX+32,self.posY:self.posY+32]
                roi[np.where(pl_img_)] = 0
                roi += pl_img
            else:
                img = self.imgp[0].copy()
                # img = cv2.rectangle(img, (self.posX,self.posY),(self.posX+20,self.posY+20) , (255, 255, 0),-1)
                # output = cv2.addWeighted(img[self.posX:self.posX+32,self.posY:self.posY+32],1, pl_img, 0.6,0)
                roi = img[self.posX:self.posX+32,self.posY:self.posY+32]
                roi[np.where(pl_img_)] = 0
                roi += pl_img
        except Exception as e:
            print(e)
        return img

game = game('background.png')
player = player('ahmed',10,10)
pl_img, ga_img ,bl_img = read_img('1.png','2.png','plane.png')
pl_img_ ,ga_img_ ,bl_img_ = preprocessing_image(pl_img,ga_img,bl_img)
game.run()
