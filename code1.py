

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:00:43 2019

@author: ebruk
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout,QDesktopWidget, QWidget,QTableWidget,QTableView,QTableWidgetItem,QHeaderView,QGraphicsScene,QGraphicsPixmapItem,QFileDialog
import pandas as pd
import openpyxl
from tasarim1 import Ui_Dialog
from sklearn.externals import joblib
from PIL import Image
from PIL import ImageQt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
import numpy as np
import matplotlib.image as mpimg
from skimage import color
from skimage import io
import matplotlib.patches as mpatches
from skimage.transform import resize
import cv2
import sqlite3
import datetime
import random
from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import numpy as np
import math
import mse_hesapla
import psnr_hesapla
import ssim_hesapla

    

class MainWindow(QWidget,Ui_Dialog):
    file_path= ""
    file_path1=""
    seciliSinif=""
    changedItems=""
    eklenecek_resim=""
    eklenecek_resim1=""
    image_list=[]
    bul_img=""
    sonuc_img=""
    seciliYuz=""
    veri_sayisi=0

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        
        self.giris.clicked.connect(self.giris_yap)
        self.g_ekle.clicked.connect(self.tuz_biber_ekle)
        self.KameraAc.clicked.connect(self.openCamera)
        self.KameraAc_2.clicked.connect(self.openCamera_2)
        self.FotografCek.clicked.connect(self.fotoCek)
        self.FotografCek_2.clicked.connect(self.fotoCek_2)
        self.ekle.clicked.connect(self.ogrEkle)
        self.mse_button.clicked.connect(self.m_hesap)
        self.psnr_button.clicked.connect(self.p_hesap)
        self.ssim_button.clicked.connect(self.s_hesap)
        self.comboBox.activated[str].connect(self.seciliSinifiBul)
        self.comboBox_3.activated[str].connect(self.seciliyuzuBul)
        self.ogr_list.itemSelectionChanged.connect(self.log_change)
        vt = sqlite3.connect('yuz_proje.db')
        im = vt.cursor()
        im.execute("""SELECT * FROM siniflar""") 
        for i in im:         
            self.comboBox.addItem(str(i[1]))
            self.comboBox_2.addItem(str(i[1]))
        vt.close()
        
    def giris_yap(self):
         try:
          sqliteConnection = sqlite3.connect('yuz_proje.db')
          id1=0
          a=""
          b=""
          cursor = sqliteConnection.cursor()
          kullanici_a=str(self.k_adi.text())
          kullanici_s=str(self.sf.text())

          query = """SELECT id,k_adi,sifre FROM personel"""
          cursor.execute(query)
          record = cursor.fetchall()
          for row in record:
              id1=row[0]
              a=row[1]
              b=row[2]
             
          if int(id1)==1:
                 if str(a)==kullanici_a and str(b)==kullanici_s:
                      self.tabWidget.setTabEnabled(1,True)
                      self.tabWidget.setTabEnabled(2, True)
                      self.mesaj.setText("Giriş Başarılı")
                      self.tabWidget.setTabEnabled(0, False)
                 else:
                      self.mesaj.setText("Eksik veya Hatalı Bilgi")
              
          cursor.close()
         finally:
           if (sqliteConnection):
            sqliteConnection.close()
            
        
        
    def ogrEkle(self):
        tc_bilgi=str(self.tc.text())
        ad_bilgi=str(self.ad_soyad.text())
        sinif_bilgi=str(self.comboBox_2.currentText())
        resim_yol=self.eklenecek_resim
        self.veritabanina_ekle(tc_bilgi,ad_bilgi,resim_yol,sinif_bilgi)
        
    def veritabanina_ekle(self,tc1,ad1,image_yol,snf):
        try:
         sqliteConnection = sqlite3.connect('yuz_proje.db')
         cursor = sqliteConnection.cursor()
         
         query_string = """ INSERT INTO ogrenci
                                  (tc,ogr_adi_soyadi,foto,sinif) VALUES (?, ?, ?, ?)"""

         foto_yol = self.BinaryData(image_yol)
         data = (tc1,ad1,foto_yol,snf)
         cursor.execute(query_string, data)
         sqliteConnection.commit()
        finally:
          if (sqliteConnection):
            sqliteConnection.close()
            self.tc.setText("")
            self.ad_soyad.setText("")
            self.label_3.setPixmap(QtGui.QPixmap("./resimler/siyah.png"))
            
    def BinaryData(self,yol):
        with open(yol, 'rb') as file:
          blob = file.read()
        return blob    
    def openCamera(self):
        camera=True
        faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eyeCascade=cv2.CascadeClassifier('haarcascade_eye.xml')
        cap=cv2.VideoCapture(0)
        '''
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,500)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,400)
        '''
        temp_img=None
        while(camera):
            ret,frame=cap.read()
            roi=frame
            gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            temp_img=gray
            faces=faceCascade.detectMultiScale(gray,1.1,7)
            eyes=eyeCascade.detectMultiScale(gray,1.1,7)
            for(x,y,w,h) in faces:
                cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),2)
            
                for (x1,y1,w1,h1) in eyes:
                  #if(y/2*x<y1*x1):
                  cv2.rectangle(roi,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
            cv2.imshow('img',roi)
            sayac=0
            for(x,y,w,h) in faces:
                cv2.rectangle(roi,(x,y),(x+w,y+h),(255,0,0),2)
                sayac+=1
                crop_img=roi[y:y+h,x:x+w]
                save_file_name=("bulunan_yuz_"+str(sayac)+'.png')
                cv2.imwrite("./resimler/"+save_file_name,crop_img)
            
            
            if cv2.waitKey(1)& 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
    def fotoCek(self):
        faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        kamera=cv2.VideoCapture(0)
        te,frame1=kamera.read()
        roin=frame1
        cv2.imwrite("./resimler/foto.png",frame1)
        self.file_path='./resimler/foto.png'
        self.label_3.setPixmap(QtGui.QPixmap(self.file_path))
        gray=cv2.cvtColor(roin,cv2.COLOR_BGR2GRAY)
        temp_img=gray
        faces=faceCascade.detectMultiScale(gray,1.1,7)
        sayac=0
        for(x,y,w,h) in faces:
                cv2.rectangle(roin,(x,y),(x+w,y+h),(255,0,0),2)
                sayac+=1
                crop_img=roin[y:y+h,x:x+w]
                save_file_name=("kaydedilen"+str(sayac)+'.png')
                cv2.imwrite("./resimler/"+save_file_name,crop_img)
        self.eklenecek_resim="./resimler/kaydedilen1.png"
        
       
    
    def seciliSinifiBul(self, text):
        self.seciliSinif = text
        self.OgrencileriGetir(self.seciliSinif)
 
    def OgrencileriGetir(self,sinif):
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        oku=im2.execute("""SELECT ogr_adi_soyadi FROM ogrenci WHERE ogrenci.sinif='"""+str(sinif)+"""'""")
        columnListe=[]
        x=im2.fetchall()
        self.ogr_list.clear()
        self.ogr_list.setColumnCount(1)
        self.veri_sayisi=len(x)
        self.ogr_list.setRowCount(self.veri_sayisi)
        for c in range(0,1):
          columnListe.append(str(c))
        self.ogr_list.setHorizontalHeaderLabels(columnListe)
        for i,row in enumerate(x):
         for j,cell in enumerate(row):
           self.ogr_list.setItem(i,j, QTableWidgetItem(str(cell)))
        vt2.close()
    def log_change(self):
           items = self.ogr_list.selectedItems()
           print(str(items[0].text()))
           a=str(items[0].text())
           self.OgrenciYuzuBul(a)
    def OgrenciYuzuBul(self,ad_soyad_1):
        try:
         sqliteConnection = sqlite3.connect('yuz_proje.db')
         cursor = sqliteConnection.cursor()
         sql_fetch_blob_query = """SELECT tc,foto FROM ogrenci WHERE ogrenci.ogr_adi_soyadi = ?"""
         cursor.execute(sql_fetch_blob_query, (ad_soyad_1,))
         record = cursor.fetchall()
         for row in record:
            tc=row[0]
            foto= row[1]
            photoPath = "./resimler/" + tc + ".png"
            self.writeTofile(foto, photoPath)
        finally:
         if (sqliteConnection):
            sqliteConnection.close()
    def writeTofile(self,data, filename):
      
      with open(filename, 'wb') as file:
        file.write(data)
      self.label_9.setPixmap(QtGui.QPixmap(filename))
      
    def seciliyuzuBul(self, text):
        self.seciliYuz=str(self.comboBox_3.currentText())
        print(str(self.seciliYuz))
        self.eklenecek_resim1=self.seciliYuz
        self.label_12.setPixmap(QtGui.QPixmap(self.eklenecek_resim1))
      
      
      
      
    def openCamera_2(self):
        camera1=True
        faceCascade1=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eyeCascade1=cv2.CascadeClassifier('haarcascade_eye.xml')
        cap1=cv2.VideoCapture(0)
        '''
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,500)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,400)
        '''
        temp_img1=None
        while(camera1):
            ret1,frame11=cap1.read()
            roi1=frame11
            gray1=cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
            temp_img1=gray1
            faces1=faceCascade1.detectMultiScale(gray1,1.1,7)
            eyes1=eyeCascade1.detectMultiScale(gray1,1.1,7)
            for(x,y,w,h) in faces1:
                cv2.rectangle(roi1,(x,y),(x+w,y+h),(255,0,0),2)
            
                for (x1,y1,w1,h1) in eyes1:
                  #if(y/2*x<y1*x1):
                  cv2.rectangle(roi1,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
            cv2.imshow('img',roi1)
            sayac1=0
            for(x,y,w,h) in faces1:
                cv2.rectangle(roi1,(x,y),(x+w,y+h),(255,0,0),2)
                sayac1+=1
                crop_img1=roi1[y:y+h,x:x+w]
                save_file_name1=("bulunan_yuzler_"+str(sayac1)+'.png')
                cv2.imwrite("./resimler/"+save_file_name1,crop_img1)
                
            
            
            if cv2.waitKey(1)& 0xFF == ord('q'):
                break
        
        cap1.release()
        cv2.destroyAllWindows()
        
    def fotoCek_2(self):
        faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        kamera=cv2.VideoCapture(0)
        te,frame1=kamera.read()
        roin=frame1
        cv2.imwrite("./resimler/foto1.png",frame1)
        self.file_path1='./resimler/foto1.png'
        self.label_11.setPixmap(QtGui.QPixmap(self.file_path1))
        gray=cv2.cvtColor(roin,cv2.COLOR_BGR2GRAY)
        temp_img=gray
        faces=faceCascade.detectMultiScale(gray,1.1,7)
        sayac=0
        self.image_list=[]
        for(x,y,w,h) in faces:
                cv2.rectangle(roin,(x,y),(x+w,y+h),(255,0,0),2)
                sayac+=1
                crop_img=roin[y:y+h,x:x+w]
                save_file_name=("kaydedilen1"+str(sayac)+'.png')
                cv2.imwrite("./resimler/"+save_file_name,crop_img)
                self.image_list.append("./resimler/"+save_file_name)
                
        print (self.image_list,len(self.image_list))        
        if len(self.image_list)==1:
            self.eklenecek_resim1=self.image_list[0]
            self.label_12.setPixmap(QtGui.QPixmap(self.eklenecek_resim1))
        elif len(self.image_list)>1:
            for i in range (0,len(self.image_list)):
                self.comboBox_3.addItem(str(self.image_list[i]))
                
            
      
              
    
        
    def tuz_biber_ekle(self):
        rastgele_beyaz=[]
        rastgele_siyah=[]
        self.deger.setText(str(self.slider.value()))
        a=int(self.deger.text())
        image1=cv2.imread(self.eklenecek_resim1)
        width,height=image1.shape[:2]
        oran=int((width*height*a)/200)
        for i in range(0,oran):
            x=random.randint(0,width)
            y=random.randint(0,height)
            if [x,y] not in rastgele_beyaz and [x,y] not in rastgele_siyah:
                rastgele_beyaz.append([x,y])
            else:
                i-=1
        for i in range(0,oran):
            x=random.randint(0,width)
            y=random.randint(0,height)
            if [x,y] not in rastgele_siyah and [x,y] not in rastgele_beyaz:
                rastgele_siyah.append([x,y])  
            else:
                i-=1
        for i in range (width):
           for j in range (height):
               if [i,j] in rastgele_beyaz:
                   image1[i,j]=255
               elif [i,j] in rastgele_siyah:
                   image1[i,j]=0
                   
        cv2.imwrite('./resimler/tuz_biber.png',image1) 
        self.eklenecek_resim1='./resimler/tuz_biber.png'
        self.label_12.setPixmap(QtGui.QPixmap(self.eklenecek_resim1))    
    
    def m_hesap(self):
        self.ogr_list2.clear()
        tc=""
        best_mse=0
        best_img=""
        img1=cv2.imread(self.eklenecek_resim1,0)
        eklenecek_tc=""
        zaman= datetime.datetime.today()
        durum="yok"
        tarih=zaman.strftime("%d-%B-%Y")
        tarih2=zaman.strftime("%d-%B-%Y %H:%M:%S")
        
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        im2.execute("""SELECT * FROM ogrenci WHERE ogrenci.sinif='"""+str(self.seciliSinif)+"""'""")
        x=im2.fetchall()
        for i in x:
            tc=i[0]
            yol="./resimler/aranan" + tc + ".png"
            image = i[2]
            self.writeTofile2(image, yol)
            img2=cv2.imread(self.bul_img,0)
            img1=resize(img1,(256,256))
            img2=resize(img2,(256,256))
            err=mse_hesapla.calculate_mse(img1, img2)
            if i==0:
                best_mse=err
                best_img=self.bul_img
                eklenecek_tc=i[0]
            else:
                if err>best_mse:
                    best_mse=err
                    best_img=self.bul_img
                    eklenecek_tc=i[0]
           
            
            vt4 = sqlite3.connect('yuz_proje.db')
            im4 = vt4.cursor()
            im4.execute("""INSERT INTO  devamsizlik (tarih,tarih_saat,ogr_tc,var_yok) VALUES ('"""+str(tarih)+"""','"""+str(tarih2)+"""', '"""+tc+"""','"""+durum+"""')""")   
            vt4.commit()
            vt4.close()
            
            
        best_mse=100-((round(int(best_mse*100)*100,14))/100)
       
        
        vt2.close()
        self.m_deger.setText(str(best_mse))       
         
        if best_mse<75: 
            self.label.setText("Öğrenci Bulunamadı")
            self.label_2.setText("")
            self.sonuc.setPixmap(QtGui.QPixmap("./siyah.png"))
            self.label_6.setText("")
            self.label_8.setText("")
        else:
         durum="var"
         self.sonuc_img=best_img
         self.sonuc.setPixmap(QtGui.QPixmap(self.sonuc_img))
         sqliteConnection = sqlite3.connect('yuz_proje.db')
         cursor = sqliteConnection.cursor()
         sql_update_query = """Update devamsizlik set var_yok = ? where ogr_tc= ? and tarih_saat=?"""
         data = (durum,str(eklenecek_tc),str(tarih2))
         cursor.execute(sql_update_query, data)
         sqliteConnection.commit()
         cursor.close()
         self.label.setText("Öğrenci Burada")
         self.label_2.setText(str(tarih2))
         self.devamsizlik_gor(eklenecek_tc)
        self.OgrencileriGetir2(tarih2)
    
    def p_hesap(self):
        self.ogr_list2.clear()
        tc=""
        best_psnr=0
        best_img=""
        img1=cv2.imread(self.eklenecek_resim1,0)
        eklenecek_tc=""
        zaman= datetime.datetime.today()
        durum="yok"
        tarih=zaman.strftime("%d-%B-%Y") 
        tarih2=zaman.strftime("%d-%B-%Y %H:%M:%S")
        
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        im2.execute("""SELECT * FROM ogrenci WHERE ogrenci.sinif='"""+str(self.seciliSinif)+"""'""")
        x=im2.fetchall()
        for i in x:
            tc=i[0]
            yol="./resimler/aranan" + tc + ".png"
            image = i[2]
            self.writeTofile2(image, yol)
            img2=cv2.imread(self.bul_img,0)
            img1=resize(img1,(256,256))
            img2=resize(img2,(256,256))
            err=psnr_hesapla.calculate_psnr(img1, img2)
            if i==0:
                best_psnr=err
                best_img=self.bul_img
                eklenecek_tc=i[0]
            else:
                if err>best_psnr:
                    best_psnr=err
                    best_img=self.bul_img
                    eklenecek_tc=i[0]
           
            
            vt4 = sqlite3.connect('yuz_proje.db')
            im4 = vt4.cursor()
            im4.execute("""INSERT INTO  devamsizlik (tarih,tarih_saat,ogr_tc,var_yok) VALUES ('"""+str(tarih)+"""','"""+str(tarih2)+"""','"""+tc+"""','"""+durum+"""')""")   
            vt4.commit()
            vt4.close()
            
            
        best_psnr=(round(int(best_psnr)*100,24))/100
        #best_psnr=(round(int(best_psnr)*100,2))/100
        self.p_deger.setText(str(best_psnr))       
        
        vt2.close()
        if best_psnr<60: 
            self.label.setText("Öğrenci Bulunamadı")
            self.label_2.setText("")
            self.sonuc.setPixmap(QtGui.QPixmap("./siyah.png"))
            self.label_6.setText("")
            self.label_8.setText("")
            
        else:
         durum="var"
         self.sonuc_img=best_img
         self.sonuc.setPixmap(QtGui.QPixmap(self.sonuc_img))
         sqliteConnection = sqlite3.connect('yuz_proje.db')
         cursor = sqliteConnection.cursor()
         
         sql_update_query = """Update devamsizlik set var_yok = ? where ogr_tc= ? and tarih_saat=?"""
         data = (durum,str(eklenecek_tc),str(tarih2))
         cursor.execute(sql_update_query, data)
         sqliteConnection.commit()
         cursor.close()
        
         self.label.setText("Öğrenci Burada") 
         
         self.label_2.setText(str(tarih2))
         self.devamsizlik_gor(eklenecek_tc)
        self.OgrencileriGetir2(tarih2)
        
    
    def s_hesap(self):
        self.ogr_list2.clear()
        
        tc=""
        best_ssim=0
        best_img=""
        img1=cv2.imread(self.eklenecek_resim1,0)
        eklenecek_tc=""
        zaman= datetime.datetime.today()
        durum="yok"
        tarih=zaman.strftime("%d-%B-%Y") 
        tarih2=zaman.strftime("%d-%B-%Y %H:%M:%S")
        
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        im2.execute("""SELECT * FROM ogrenci WHERE ogrenci.sinif='"""+str(self.seciliSinif)+"""'""")
        x=im2.fetchall()
        for i in x:
            tc= i[0] 
            yol="./resimler/aranan" + tc + ".png"
            image = i[2]
            self.writeTofile2(image, yol)
            img2=cv2.imread(self.bul_img,0)
            img1=resize(img1,(256,256))
            img2=resize(img2,(256,256))
            err=ssim_hesapla.calculate_ssim(img1, img2)
            if i==0:
                best_ssim=err
                best_img=self.bul_img
                eklenecek_tc=i[0]
            else:
                if err>best_ssim:
                    best_ssim=err
                    best_img=self.bul_img
                    eklenecek_tc=i[0]
            vt4 = sqlite3.connect('yuz_proje.db')
            im4 = vt4.cursor()
            im4.execute("""INSERT INTO  devamsizlik (tarih,tarih_saat,ogr_tc,var_yok) VALUES ('"""+str(tarih)+"""','"""+str(tarih2)+"""', '"""+tc+"""','"""+durum+"""')""")   
            vt4.commit()
            vt4.close()
            
         
        best_ssim=(round(int(best_ssim*100)*100,2))/100
        self.s_deger.setText(str(best_ssim))       
        
        vt2.close()
        if best_ssim<60: 
            self.label.setText("Öğrenci Bulunamadı")
            self.label_2.setText("")
            self.sonuc.setPixmap(QtGui.QPixmap("./siyah.png"))
            self.label_6.setText("")
            self.label_8.setText("")
        else:
         durum="var"
         self.sonuc_img=best_img
         self.sonuc.setPixmap(QtGui.QPixmap(self.sonuc_img))
         sqliteConnection = sqlite3.connect('yuz_proje.db')
         cursor = sqliteConnection.cursor()
         
         sql_update_query = """Update devamsizlik set var_yok = ? where ogr_tc= ? and tarih_saat=?"""
         data = (durum,str(eklenecek_tc),str(tarih2))
         cursor.execute(sql_update_query, data)
         sqliteConnection.commit()
         cursor.close()
        
         self.label.setText("Öğrenci Burada")  
          
         self.label_2.setText(str(tarih2))
         self.devamsizlik_gor(eklenecek_tc)
        self.OgrencileriGetir2(tarih2)    
    
    
    def writeTofile2(self,data, filename):
      # Convert binary data to proper format and write it on Hard Disk
      with open(filename, 'wb') as file:
        file.write(data)
      print("Stored blob data into: ", filename, "\n")
      self.bul_img=filename  
      
    def OgrencileriGetir2(self,zaman):
        sinif=self.seciliSinif
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        im2.execute("""SELECT ogrenci.tc,ogrenci.ogr_adi_soyadi,devamsizlik.var_yok,devamsizlik.tarih_saat from ogrenci inner join devamsizlik on ogrenci.tc=devamsizlik.ogr_tc where ogrenci.sinif='"""+str(sinif)+"""'and devamsizlik.tarih_saat='"""+str(zaman)+"""'""")
        columnListe=[]
        x=im2.fetchall()
        self.ogr_list2.clear()
        self.ogr_list2.setColumnCount(4)
        self.ogr_list2.setRowCount(len(x))
        for c in range(0,1):
          columnListe.append(str(c))
        self.ogr_list2.setHorizontalHeaderLabels(columnListe)
        for i,row in enumerate(x):
         for j,cell in enumerate(row):
           self.ogr_list2.setItem(i,j, QTableWidgetItem(str(cell)))
        vt2.close()
        
    def devamsizlik_gor(self,tc):
        geldi=0
        vt2 = sqlite3.connect('yuz_proje.db')
        im2 = vt2.cursor()     
        im2.execute("""SELECT COUNT(DISTINCT devamsizlik.tarih) FROM devamsizlik WHERE devamsizlik.var_yok="var" and  devamsizlik.ogr_tc='"""+str(tc)+"""'""")
        x=im2.fetchall()
        for i in x:
            geldi=i[0]
        self.label_6.setText(str(geldi))
        vt2.close()
        
        gelmedi=0
        vt3 = sqlite3.connect('yuz_proje.db')
        im3 = vt3.cursor()     
        im3.execute("""SELECT COUNT(DISTINCT devamsizlik.tarih) FROM devamsizlik WHERE devamsizlik.var_yok="yok" and  devamsizlik.ogr_tc='"""+str(tc)+"""'""")
        y=im3.fetchall()
        for j in y:
            gelmedi=j[0]
        self.label_8.setText(str(gelmedi))
        vt3.close()
        
        
        