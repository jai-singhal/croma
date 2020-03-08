import os, sys
from django.conf import settings
from accounts.models import Registration

def print_header(fp, sale_info):
  reg = Registration.objects.first()

  fp.write('\n{0:26}{1:20}\n'.format(" ", "GST INVOICE"))

  fp.write('   {0:28}{1:4}{2}\n'.format("DL No: " + 
              (reg.dl_no1.upper() if reg.dl_no1 else ""), "   ", " GST No.: " + (reg.gst_no if reg.gst_no else "")))
  fp.write('{0:17}{1}\n'.format(" ", reg.company_name.upper() if reg.company_name else ""))
  fp.write('   {0:38}{1}\n'.format(
                          (reg.address1.upper() if reg.address1 else "")
                           +  ( "," + reg.address2.upper() if reg.address2 else "")
                            + ( "," + reg.city.upper() if reg.city else ""), 
                            "    Ph.: " + (reg.phone1 if reg.phone1 else "")))
  fp.write('  ' + '-'*60 + '\n')
  fp.write('   {0:9}{1:30}{2:11}{3}\n'.format("Patient:  ", sale_info['party_id'][:26], "Invoice No: ", sale_info['inv_no']))
  doc_dt = sale_info['doc_dt'].split("-")
  doc_dt = doc_dt[2] + "/" + doc_dt[1] + "/" + doc_dt[0]

  fp.write('   {0:10}{1:30}{2:}{3}\n'.format("Presc.by: ", sale_info['doctor_id'][:25], "Date: ", doc_dt))
  fp.write('  ' + '-'*60 + '\n')
  fp.write('{0:5}{1:5}{2:25}{3:11}{4:8}{5}\n'.format(" ", "Qty", "Name of Item", "Batch No.", "Expiry", "Amount"))
  fp.write('  ' + '-'*60 + '\n')


def print_footer(fp, sale_info):
  reg = Registration.objects.first()
  fp.write('  ' + '-'*60 + '\n')

  fp.write('  {0:4}{1:7}'.format("   Item: ", str(sale_info['total_item'])))
  fp.write('{0:5}{1:10}'.format("Disc:", str(sale_info['sale_discount'])))
  fp.write('{0:5}{1:9}'.format("Adj:", str(0.00)))
  fp.write('{0:6}{1:10}\n'.format("Total: ", str(sale_info['net_amount'])))

  fp.write('  ' + '-'*60 + '\n')
  company_name = reg.company_name.title().split(" ")
  footer = " Consult your Doctor before use. For " \
          + ( " ".join(company_name) if reg.company_name else "") + \
            ". Price includes Reimb. for GST paid"
  # print(len(footer)/2)
  fp.write('   {0}\n'.format(footer[0:53]))
  fp.write('   {0}\n'.format(footer[53:]))


def print_items(fp, sale_items, page_no):
  x = 0
  if(page_no > 1):
   x = (page_no - 1)*6

  for item in sale_items[x : page_no*6]:

    fp.write('{0:6}{1:4}'.format(" ", str(item['qty'])))
    item_name = item['item_name']

    if(len(item['item_name']) >= 25):
      item_name = item['item_name'][0:23] + ".."

    fp.write('{:25}'.format(item_name))

    batch = item['batch']
    if(len(item['batch']) >= 11):
      batch = item['batch'][0:9] + ".."

    fp.write('{:11}'.format(batch))

    expiry = item['expiry'][0:7].split("-")
    expiry = expiry[1] + "/" + expiry[0]
    fp.write('{:8}'.format(expiry))
    fp.write('{:0.2f}\n'.format(float(item['amount'])))

  for i in range(len(sale_items), 6*page_no):
    fp.write("\n")


def MakeInvoice(json_dict):
  sale_items = json_dict['sale_item']
  sale_info = json_dict['sale_info']

  file_path = getattr(settings, "PRINTINV_FILEPATH", None)

  fp = open(file_path, "w")

  total_items = int(sale_info['total_item'])
  total_pages = total_items//6 + 1
  if(total_items%6 == 0):
    total_pages = total_items//6

  page_count = 1
  if total_pages == 0:
       print_header(fp, sale_info) 

  while(total_pages >= page_count):

    print_header(fp, sale_info)
    print_items(fp, sale_items, page_count)

    if(page_count != total_pages):
      fp.write('{0:43}{1:12}'.format(" ", "Continued on... " + str(page_count + 1)))
      fp.write("\n"*6)
    page_count += 1


  print_footer(fp, sale_info)
  fp.close()
