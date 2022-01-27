from itertools import islice
import re
from tika import parser  # pip install tika
import pandas as pd
import numpy

file = r"https://bijakteaminternal-userfiles-mobilehub-429986086.s3.ap-south-1.amazonaws.com/public/order/11263025_20211104_015903_1636025800697.pdf"

poPdfLinks = pd.read_csv('../pdf_parsing.csv')
pdfLinksArr = poPdfLinks["aa"].values

cols = ['Item Code', 'HSN Code', 'Product UPC', 'Product Description', 'Basic Cost Price',
        'IGST %', 'CESS%', 'Tax Amt', 'Landing Rate', 'QTY.', 'MRP', 'Margin%', 'Total Amt', 'PDF link']

cols2 = ['Item Code', 'HSN Code', 'Product UPC', 'Product Description', 'Basic Cost Price',
         'IGST %', 'SGST%', 'CESS%', 'Tax Amt', 'Landing Rate', 'QTY.', 'MRP', 'Margin%', 'Total Amt', 'PDF link']

cols3 = ['Item Code', 'HSN Code', 'Product UPC', 'Product Description', 'Basic Cost Price',
         'IGST %', 'SGST%', 'CESS%', 'ADDT. CESS', 'Tax Amt', 'Landing Rate', 'QTY.', 'MRP', 'Margin%', 'Total Amt', 'PDF link']

def is_float(element) -> bool:
  try:
      float(element)
      return True
  except ValueError:
      return False

def pdfToDataframe(file):
  raw = parser.from_file(file)
  pdfContent = raw['content'].strip('\n')
  stringPdf = repr(pdfContent)
  stringPdf = stringPdf.replace(r'\n\n', ' ')
  stringPdf = stringPdf.replace(r'\n', '').strip()
  res = re.search('TotalAmt(.*)Total Quantity:', stringPdf)
  rowsStr = res.group(1)
  print('shivam',rowsStr);
  rowsStr = rowsStr.replace(r'\n\n', ' ')
  rowsStr = rowsStr.replace(r'\n', '').strip()
  rowsStr = rowsStr.replace(r' (', r'(')
  rowsStr = rowsStr.replace(' g)', 'g)')
  rowsStr = rowsStr.replace(' gm)', 'gm)')
  rowsStr = rowsStr.replace(' kg)', 'kg)')
  rowsStr = rowsStr.replace('g - ', 'g-')
  rowsStr = rowsStr.replace('  ', ' ')
  rowsStr = rowsStr.replace(') - ', ')-')
  rowsStr = rowsStr.replace(') -', ')-')
  rowsArr = rowsStr.split(' ')
  csvArr = []
  csvRowArr = []
  rowCount = 0
  i = 0;
  totalCols = 13;
  while i < len(rowsArr):
    if rowsArr[i].isdigit() and int(rowsArr[i]) == rowCount + 1:
      rowCount += 1
      if(len(csvRowArr) > 0):
        csvRowArr.append(file);
        print(csvRowArr);
        csvArr.append(csvRowArr)
        csvRowArr = []
      i += 1;
      continue
    elif is_float(rowsArr[i]) or rowsArr[i].isdigit():
      csvRowArr.append(rowsArr[i])
    else:
      csvLastIndex = len(csvRowArr) - 1
      if is_float(rowsArr[i-1]) or rowsArr[i-1].isdigit():
        csvLastIndex = len(csvRowArr);
        csvRowArr.append('');
      csvRowArr[csvLastIndex] = csvRowArr[csvLastIndex] + ' ' + rowsArr[i]
    i += 1;
  
  csvRowArr.append(file);
  totalCols = len(csvRowArr);
  csvArr.append(csvRowArr);
  
  finalReturn = [totalCols];
  if(totalCols == 14):
    df = pd.DataFrame(csvArr, columns=cols);
    finalReturn.append(df)
  elif(totalCols == 15): 
    df = pd.DataFrame(csvArr, columns=cols2);
    finalReturn.append(df);
  else:
    df = pd.DataFrame(csvArr, columns=cols3);
    finalReturn.append(df);

  return finalReturn;

dfs=[];
dfs2=[];
dfs3=[];
for pdf in pdfLinksArr:
  print("file", pdf);
  pdfData = pdfToDataframe(pdf);
  if(pdfData[0] == 14):
    dfs.append(pdfData[1]);
  elif(pdfData[0] == 15):
     dfs2.append(pdfData[1]);
  else:
     dfs3.append(pdfData[1]);


final = pd.concat(dfs);
final2 = pd.concat(dfs2);
final3 = pd.concat(dfs3);

final.to_csv('pdf1ToExcel.csv');
final2.to_csv('pdf2ToExcel.csv');
final3.to_csv('pdf3ToExcel.csv');
# rowsStr = rowsStr.replace(r'\n\n', ' ')
# rowsStr = rowsStr.replace(r'\n', '').strip()
# print(pdfContent);
# print('shivamm',stringPdf);
# print('shivamm',res);
# print('shivamm', rowsStr)
# print('shivamm', int('78'))
# res = re.search('PO GRN(.*)Total Quantity in PO', repr(pdfContent))
