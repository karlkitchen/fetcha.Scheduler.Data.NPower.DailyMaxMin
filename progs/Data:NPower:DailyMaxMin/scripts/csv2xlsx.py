## -*- coding: utf-8 -*-

import sys
sys.path.append('/project/fetcha/libs/XlsxWriter-RELEASE_0.9.3')
import xlsxwriter

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if len(sys.argv)!=4:
  print ("__WIM_FAIL: Incorrect number of arguments")
  status=2
  exit(status)

filename_in  = sys.argv[1]
filename_out = sys.argv[2]
tabname      = sys.argv[3]

workbook = xlsxwriter.Workbook(filename_out)
worksheet = workbook.add_worksheet(tabname)

worksheet.set_column('A:A',20)
worksheet.set_column('B:B',20)
worksheet.set_column('C:C',20)

format = workbook.add_format()
format.set_font_name('sans-serif')
format.set_font_size('10')
format.set_align('right')

date_format = workbook.add_format()
date_format.set_font_name('sans-serif')
date_format.set_font_size('10')

format_flt=workbook.add_format({'num_format': '0.0'})
format_int=workbook.add_format({'num_format': '0'})

bold = workbook.add_format({'bold': True})
bold.set_font_name('sans-serif')
bold.set_font_size('10')

bg_fill = workbook.add_format({'bg_color': '#C0C0C0','valign': 'top'})
bg_fill.set_font_name('sans-serif')
bg_fill.set_font_size('10')

fh_in=open(filename_in,'r')
contents=fh_in.readlines()

text=0
row=0
for line in contents:
  column=0

  date_test=(len(line.split(',')[0].split('/')) == 3)
  if (text <= 0 and not date_test):
    if (row == 0):
      text=6
    else:
      text=8
  else:
    text=text-1
    
  for raw_row_data in line.split(','):
    row_data=raw_row_data.strip()
    if (text >= 3 and text <= 6):
      worksheet.write(row,column,row_data,bold)
    elif (text > 0 and text <= 2):
      worksheet.write(row,column,row_data,bg_fill)
    else:
      if (is_number(row_data)):
        if (column == 1 or column == 2):
          worksheet.write_number(row,column,float(row_data),format_flt)
        else:
          worksheet.write_number(row,column,float(row_data),format_int)
      else:
        if (column == 0):
          worksheet.write(row,column,row_data,date_format)
        else:
          worksheet.write(row,column,row_data,format)
    column=column+1
  row=row+1

fh_in.close()

workbook.close()
