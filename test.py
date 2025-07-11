from PIL import Image
import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\PRAVSAG\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Load the image directly
img = Image.open("C:/Users/PRAVSAG/Downloads/pie chart -00001.png")
text = pytesseract.image_to_string(img)
with open('demo.txt','w') as file:
    file.writelines(text)
with open('demo.txt','r') as file:
    data = file.readlines()
    ed = [i.replace('\n','') for i in data if '\n' in i]
    print(ed, len(ed))
# print("Extracted text:")
# print(text)
