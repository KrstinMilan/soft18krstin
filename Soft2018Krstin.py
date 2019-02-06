# Milan Krstin
# e13642

class Blob:
    def __init__(self,bID,x,y,age,death):
        self.x = x
        self.y = y
        self.bID = bID
        self.age = age
        self.death = death
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def setX(self, xb):
        self.x = xb

    def setY(self, yb):
        self.y = yb

    def getAge(self):
        return self.age
    
    def setAge(self):
        self.age += 1   

    def getDeath(self):
        return self.death
        
    def setDeath(self):
        self.death +=1

def correctSize(area):
    if (area > 25 and area < 330):
        return True
    else: return False

def sameDude(x,xx, y, yy):
    if abs(x-xx) <= 25 and abs(y-yy) <= 35:
        return True
    else: return False

def naPlatou(y):
    h=cap.get(4)
    if y >= h*0.25 and y <= h*0.9:
        return True
    else: return False

import cv2
import numpy as np
import os

if os.path.exists("out.txt"):
    os.remove("out.txt")

f= open("out.txt","w+")
f.write("e13642,Milan Krstin\n")
f.write("file,count\n")
f.close()
resenja = [4, 25, 16, 23, 17, 27, 28, 22, 10, 22]

#pistanje svakog videa
for b in range(10):
    video = f"video{b+1}.mp4"
    cap = cv2.VideoCapture(video)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    ljudi = []
    bID = 1
    age = 0
    death = 0
    brojeni = []
    brojac = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            #mask
            fgmaska = fgbg.apply(frame)
            ret,tresh = cv2.threshold(fgmaska,200,255,cv2.THRESH_BINARY)
    
            #kernel
            kernelopen = np.ones((3,3), np.uint8)
            kernelclose = np.ones((11,11), np.uint8)
            clear = cv2.morphologyEx(tresh, cv2.MORPH_OPEN, kernelopen)
            clear = cv2.morphologyEx(clear, cv2.MORPH_CLOSE, kernelclose)
            # clear = cv2.dialate(tresh, kernelopen, iterations=1)
            
            #poligon
            pts = np.array([[183,115], [473,93], [520,445], [174,455]], np.int32)
            cv2.polylines(frame, [pts], True, (150, 150, 0), 4) 
        
        except:
            break
    
        #pronalazenje kontura
        konture, stagod = cv2.findContours(clear, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for kontura in konture:
            area = cv2.contourArea(kontura)
            centerKont, sizeKont, angleKont = cv2.minAreaRect(kontura) # pronadji pravougaonik minimalne povrsine koji ce obuhvatiti celu konturu
            widthKont, heightKont = sizeKont
            if (correctSize(area)):
                M = cv2.moments(kontura)
                kx = int(M['m10']/M['m00'])
                ky = int(M['m01']/M['m00'])
                x,y,w,h = cv2.boundingRect(kontura)

                #proveravanje da li je novi ili postojeci blob
                flag = True
                for covek in ljudi:
                    if sameDude(x, covek.getX(), y, covek.getY()):   
                        flag = False
                        covek.setAge()
                        covek.setX(kx)
                        covek.setY(ky)
                        break
                    else:
                        covek.setDeath()
                if flag == True:
                    blob = Blob(bID,kx,ky,age,death)
                    ljudi.append(blob)
                    bID += 1

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        #dodavanje u brojene
        for covek in ljudi:
            if covek.getAge() > 15 and covek not in brojeni and naPlatou(covek.getY()):
                brojeni.append(covek)

        #pustanje videa
        brojac = len(brojeni)
        text = str(brojac)
        cv2.putText(frame,video,(30, 300),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'Q stop',(30, 340),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,text,(30, 410),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2,cv2.LINE_AA)
        cv2.imshow(video, frame)

        #zaustavljanje videa
        if cv2.waitKey(1) & 0xFF == ord ('q') : break #izlaz iz petlje q

    cap.release()
    cv2.destroyAllWindows()

    #odredjivanje tacnosti
    if brojac >= resenja[b]:
        tacnost = (float(resenja[b])/brojac)*100
    else:
        tacnost = (float(brojac)/resenja[b])*100

    #dodavanje u out.txt
    print (b+1,int(tacnost),'%')
    f=open("out.txt", "a")
    f.write("%s," % video)
    f.write("%d\n" % brojac)
    f.close()