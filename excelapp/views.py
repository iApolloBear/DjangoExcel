from django.shortcuts import render
import openpyxl

# Create your views here.


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
