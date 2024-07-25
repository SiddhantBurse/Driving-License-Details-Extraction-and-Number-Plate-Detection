import numpy as np
import cv2
import imutils
import pytesseract
def lisc(text):

        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\siddh\AppData\Local\Tesseract-OCR\Tesseract.exe"
        image = cv2.imread(text)
        
         
        image = cv2.resize(image,(1000,600))

        
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)

       
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("1 - Grayscale Conversion", gray)
        cv2.waitKey(0)

        
        gray1 = cv2.bilateralFilter(gray, 11, 17, 17)
        cv2.imshow("Bilateral Filter", gray1)
        cv2.waitKey(0)

        
        edged = cv2.Canny(gray1, 170, 200)
        cv2.imshow("3 - Canny Edges", edged)
        cv2.waitKey(0)

       
        cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        
        img1 = image.copy()
        cv2.drawContours(img1, cnts, -1, (0,255,0), 1)
        cv2.imshow("4- All Contours", img1)
        cv2.waitKey(0)

       
        cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
        NumberPlateCnt = None 

        
        img2 = image.copy()
        cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
        cv2.imshow("5- Top 30 Contours", img2)
        cv2.waitKey(0)

        
        count = 0
        idx =7
        for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
               
                if len(approx) == 4:  
                    NumberPlateCnt = approx 

                    
                    x, y, w, h = cv2.boundingRect(c) 
                    new_img = gray[y:y + h, x:x + w] 
                    cv2.imwrite('cropimg/' + str(idx) + '.png', new_img) 
                    idx+=1

                    break





     
        new_img= cv2.resize(new_img,(800,400))
        cv2.imshow("Cropped Image 2", new_img)
        cv2.waitKey(0)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        new_img = cv2.filter2D(new_img, -1, kernel)
        cv2.imshow("Sharp edge", new_img)
        cv2.waitKey(0)
        ret,new_img = cv2.threshold(new_img,200,255,cv2.THRESH_BINARY)
        cv2.imshow("Thresholded image", new_img)
        cv2.waitKey(0)
        #kernel = np.ones((3,3), np.uint8) 
        #er=cv2.erode(new_img,kernel,iterations=2)
        #cv2.imshow(,"Eroded image", er)
        er=np.zeros((400,800),dtype=np.uint8)
        cv2.waitKey(0)
        #ret,er = cv2.threshold(er,1,255,cv2.THRESH_BINARY)
        #cv2.imshow("Thresholded image-1", er)
        er[:57,:]=255;
        er[:,:20]=255;
        er[:255,:110]=255;
        er[:,625:]=255;
        er[95:225,:]=255;
        er[340:,:]=255;
        cv2.waitKey(0)
        new_img+=er
        cv2.imshow("Image with mask", new_img)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        new_img = cv2.filter2D(new_img, -1, kernel)
        cv2.imshow("Sharp edge1", new_img)
        cv2.waitKey(0)
        start=0
        l=[]
        text=[]
        for i in range(400):
                if start==0:
                        if 0 in new_img[i:i+1,:]:
                                start=i-3
                else:
                        if 0 not in new_img[i:i+1,:]:
                                end=i+3
                                l.append(new_img[start:end+1,:])
                                start=0
        for i in range(len(l)):
                cv2.imshow('bleh',l[i])
                cv2.waitKey(0)
                text.append(pytesseract.image_to_string(l[i], lang='eng'))
        i=0
        n=len(text)
        while i<n:
                if text[i]=='':
                        text.pop(i)
                        n-=1
                        continue
                text[i]=text[i][:len(text[i])-2]
                #print(text[i])
                
                i+=1
        i=0
        n=len(text)
        while i<n:
                if '\n'in text[i]:
                        ind=text[i].index('\n')
                        text[i]=text[i][:ind]+'\t'+text[i][ind+1:]
                        continue
                
                #print(text[i])
                i+=1
        i=0        
        while i<len(text):
                if '\t' in text[i]:
                        ind=text[i].index('\t')
                        text.insert(i+1,text[i][ind+1:])
                        text[i]=text[i][:ind]
                        
                print(text[i])
                #print('x')
                i+=1
        i=0
        while i<len(text):
                if text[i].isspace() or text[i]=='':
                        text.pop(i)
                        continue
                print(text[i])
                #print('x')
                i+=1
        text[len(text)-3]+=' '+text[len(text)-2]+' '+text[len(text)-1]
        text.pop(len(text)-1)
        text.pop(len(text)-1)
        print(text[len(text)-1])

        if len(text)>5:
                text.pop(len(text)-2)
        i=0
        while i<len(text)-2:
                j=0
                while j<len(text[i])-2:
                        if text[i][j].isnumeric() and text[i][j+1].isspace() and text[i][j+2].isalpha():
                                text.insert(i+1,text[i][j+2:])
                                text[i]=text[i][:j+1]
                                break
                        j+=1
                i+=1
        text[0]=text[0][6:]
        text[1]=text[1][5:]
        text[2]=text[2][12:]
        text[3]=text[3][4:]
        text[4]=text[4][3:]
        text[5]=text[5][5:]
        text[6]=text[6][4:]
        i=0
        while i<len(text):
                print(text[i])
                i+=1
        return text
        


