from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
import openpyxl
from .models import Client

# Create your views here.


def excel(request):
    if request.method == 'POST':
        try:
            excel_file = request.FILES['excel_file']
            if str(excel_file).split('.')[-1] == "xls":
                data = xls_get(excel_file, column_limit=5)
            elif str(excel_file).split('.')[-1] == 'xlsx':
                data = xlsx_get(excel_file, column_limit=5)
            else:
                return HttpResponse("Invalid File")

            details = data["Detalle"]
            if len(details) > 1:
                for detail in details:
                    if len(detail) > 0 and detail[0] != "Sucursal":
                        Client.objects.create(
                            sucursal=detail[0], cartera=detail[1], clientes=detail[2], fecha_alta=detail[3], saldo=detail[4])
            return HttpResponse("Data Readed")

        except MultiValueDictKeyError:
            return HttpResponse("Invalid File")
    else:
        return render(request, 'excelapp/index.html')


def index(request):
    if request.method == "GET":
        return render(request, 'excelapp/index.html')
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Detalle"]
        print(worksheet)
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        return render(request, 'excelapp/index.html', {"excel_data": excel_data})
