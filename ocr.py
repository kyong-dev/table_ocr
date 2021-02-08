import time
import easyocr
from collections import defaultdict
from PIL import Image
import mysql.connector
import ftplib
import os
import datetime

mydb = mysql.connector.connect(
  host="192.168.0.25",
  user="vvicuser",
  password="Q1w2e3r4t5y6u7i8!",
  database="vvic2",
  port="3306"
)

mycursor = mydb.cursor()
sql = "SELECT * FROM all_img WHERE ocr2 is NULL LIMIT 1"
#sql = "SELECT * FROM all_img WHERE img_no = 28"

#reader = easyocr.Reader(['ch_sim','en'])
reader = easyocr.Reader(['ch_sim'])

startTime = time.time()

def detect_chinese(str):
	for ch in str:
		if u'\u4e00' <= ch <= u'\u9fff':
			return True
	return False

#index = 1
while True:
    mycursor.execute(sql)
    imgData = list(mycursor.fetchone())

    if imgData == None:
        break

    imgNo = str(imgData[0])
    filename = str(imgData[4])

    update_sql = "UPDATE all_img SET ocr2 = ' ' WHERE img_no = " + imgNo 
    mycursor.execute(update_sql)
    mydb.commit()

    imgURL = "./Product/Img/" + str(imgData[2]) + "/" + str(imgData[1])

    print(f"{imgNo}. {imgURL}/{filename} updating...")

    i = 0
    connection = 20
    while i < connection:
        try:
            ftp = ftplib.FTP("192.168.0.25") 
            ftp.encoding = "UTF-8"

            ftp.login("graeftp", "rmfo0309!")

            ftp.cwd(imgURL)
            newImage = open("img/" + filename, 'wb')
            ftp.retrbinary("RETR " + filename, newImage.write)
            newImage.close()
            ftp.quit()
            break
        except Exception as e:
            update_sql = "UPDATE all_img SET ocr2 = NULL WHERE img_no = " + imgNo 
            mycursor.execute(update_sql)
            mydb.commit()
            time.sleep(1)
            continue

    if i != 0:
        print(f"{i} tries...")

    words = defaultdict(list)
    xPositions = []
    try:
        words = reader.readtext("img/" + filename)
    except Exception:
        pass

    output = ""
    for r in words:
        temp = r[1].replace("\'", " ")
        temp = temp.replace("\\", "")
        temp = temp.replace('\"', '\""')
        output += temp + "||"

    if detect_chinese(output) is False:
        output = ""

    #index += 1
    print(output)

    if output != "":
        update_sql = f"UPDATE all_img SET ocr2 = '{output}' WHERE img_no = {imgNo}"
        mycursor.execute(update_sql)
        mydb.commit()
    try:
        os.remove(f"img/{filename}")
        print(f"{imgNo}. {imgURL}/{filename} updated at {datetime.datetime.now()}")
    except OSError:
        print(f"{imgNo}. {imgURL}/{filename} NOT FOUND")
        pass

endTime = time.time()
print(endTime - startTime)
