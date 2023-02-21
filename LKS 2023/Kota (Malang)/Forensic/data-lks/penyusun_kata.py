import pytesseract
import cv2
image="D:\\Programming\\Cyber Security\\LKS 2023\\Kota (Malang)\\Forensic\\data-lks\\data\\img5.png"
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
text = pytesseract.image_to_string(image)
print(text)