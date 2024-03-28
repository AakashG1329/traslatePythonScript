import os
import time
from fastapi import FastAPI, File, UploadFile, HTTPException,Response
import io
import PyPDF2
import re
from pypdf import PdfReader 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

app = FastAPI()

def read_pdf_text(file):
    pdf_reader = PyPDF2.PdfFileReader(file,strict=False)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text
def create_excel_with_data(file_path, data):
    # Create a new Workbook
    wb = Workbook()

    # Select the active worksheet
    ws = wb.active

    # Add data to the worksheet
    for row in data:
        ws.append(row)

    # Save the workbook
    wb.save(file_path)
    return

# Example usage



@app.post("/pdf/text/")
async def read_pdf_text_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")
    
    pdf_content = await file.read()
    pdf_file = io.BytesIO(pdf_content)
    text = read_pdf_text(pdf_file)
    print(text)
    input_string = "3restaurant4intense5facilitate6fast7"

# Split the string based on numeric characters
    result = re.split(r'\d+', text)
    data=[]
# Remove empty strings from the result
    result = [item for item in result if item]
    # print(result)
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/search?q=english+to+tamil")
    text_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='Enter text']"))
        )
    text_output = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='tw-target-text-container']//pre/span[1]"))
        )

        # Click the button
    data = [
    ['English', 'Tamil'],]
    for val in result:
         text_input.send_keys(val)
         time.sleep(1)
         print(text_output.text) 
         data2=[val,text_output.text]
         data.append(data2)
         text_input.clear()
         print(data)
    # print(data)    
    driver.close()
    create_excel_with_data("file/Translated.xls", data) 
    output = io.BytesIO()
    
    output.seek(0)
    file_path="file/Translated.xls"

    # Set response headers for file download
   
    
    # dls = "Translated.xlsx"
    # urllib.request.urlretrieve(dls, "test.xls") 
    # Check if the file exists
    if not os.path.exists(file_path):
        return Response(content="File not found", status_code=404)
    
    # Set content disposition to 'attachment' to trigger a file download
    headers = {
        "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
    }
    
    # Return a response with the file as content and headers set
    return Response(content=open(file_path, "rb").read(), headers=headers)
# @app.post("/upload2")
# async def upload2(file: UploadFile = File(...)):


  
# # creating a pdf reader object 
#     reader = PdfReader(file) 
  
# # printing number of pages in pdf file 
#     print(len(reader.pages)) 
  
# # getting a specific page from the pdf file 
#     page = reader.pages[0] 
  
# # extracting text from page 
#     text = page.extract_text() 
#     print(text) 
#     return text