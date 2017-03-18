# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageDraw
from pytesser import image_to_string

class verify_img:
    def __init__(self, img_file=''):
        self.img_file = img_file
        self.threshold = 120
        
        self.rep={'O':'0',    
                'I':'1','L':'1',']':'1',    
                'Z':'2',    
                'S':'8','B':'8',
                'C':'0',
                };
        
    def table_2value(self):
        # 二值化
        table = []
        for i in range(256):
            if i < self.threshold:
                table.append(0)
            else:
                table.append(1)
        return table
        
    def get(self):
        im = Image.open(self.img_file)
        #im = ImageEnhance.Sharpness(im).enhance(2)
        #im.show()
        #im1 = self.test(im)
        #
        #转化到灰度图  
        imgry = im.convert('L')  
        
        self.clearNoise(im,50,4,4)
        #保存图像  
        imgry.save('g'+self.img_file)
        #imgry.show()
        #二值化，采用阈值分割法，threshold为分割点   
        out = imgry.point(self.table_2value(),'1')    
        out.save('b'+self.img_file)
        #out.show()
        #识别    
        text = image_to_string(out)
        #print 111
        #识别对吗    
        text = text.strip()    
        text = text.upper();      
        for r in self.rep:    
            text = text.replace(r,self.rep[r])     
        #print text    
        return text
    
    def test(self,img):
        pixdata = img.load()
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < 0:
                    pixdata[x, y] = (0, 0, 0, 255)
 
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)
 
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)
        #img.show()
        return img
 

    def getPixel(self,image,x,y,G,N):  
        L = image.getpixel((x,y))  
        if L > G:  
            L = True  
        else:  
            L = False  
      
        nearDots = 0  
        if L == (image.getpixel((x - 1,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x - 1,y)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x - 1,y + 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x,y + 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y - 1)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y)) > G):  
            nearDots += 1  
        if L == (image.getpixel((x + 1,y + 1)) > G):  
            nearDots += 1  
      
        if nearDots < N:  
            return image.getpixel((x,y-1))  
        else:  
            return None 
        
    def clearNoise(self, image,G,N,Z):  
        draw = ImageDraw.Draw(image)
        for i in xrange(0,Z):  
            for x in xrange(1,image.size[0] - 1): 
                for y in xrange(1,image.size[1] - 1):  
                    color = self.getPixel(image,x,y,G,N)
                    if color != None:
                        draw.point((x,y),color)  
        
if __name__ == "__main__":
    verify=verify_img(img_file='verifyimg.jpeg')
    print verify.get()
