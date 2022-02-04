# import googletrans
# from googletrans import Translator
 
# print(googletrans.LANGUAGES) # 언어 종류
 
# text1 = "Hello welcome to my website!"
# translator = Translator()
# trans1 = translator.translate(text1, src='en', dest='ja') # src -> 출발지 , dest -> 목적지
# print("English to Japanese: ", trans1.text)

import pdfplumber

with pdfplumber.open("아뱅.pdf") as pdf:
    for i in range(len(pdf.pages)):
        first_page = pdf.pages[i]
        print(first_page.extract_text())
