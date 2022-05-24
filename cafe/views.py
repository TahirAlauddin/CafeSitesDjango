from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection
from django.http import HttpResponse

from colorama import init
from colorama import Fore, Back, Style

import pandas as pd
import numpy as np
import json

from .models import Cafe, Table, Color, Record

init(autoreset=True)

@login_required
def view_create_cafe(request):
    if not request.user.is_staff:
        #? if a regular user tries to access this page, make it unaccessible 
        messages.add_message(request, level=messages.INFO, message="You aren't allowed to create a centre.")
        return redirect("home")

    if request.method == "POST":
        if request.FILES:
            image = request.FILES.get('image')
            cafe_name = request.POST.get('cafe_name')

            #? Creating Cafe object
            cafe = Cafe.objects.get(name=cafe_name)
            cafe.image = image
            cafe.save()

            messages.add_message(request, level=messages.INFO, message="Cafe saved!")

            return redirect('home')

        for i in request:
            #? Get tables positions and information from JSON
            data = json.loads(i)
            table_ids = list(data['table_ids'])
            tables_distance_top = list(data['array_distance_top'])
            tables_distance_left = list(data['array_distance_left'])
            tables_label = list(data['array_labels'])
            # tables_numbers = list(range(len(tables_label)))
            cafe_name = data['cafe_name']

            print(Fore.BLUE + str(data))
            cafe = Cafe(name=cafe_name)
            cafe.save()

            for table_id, table_distance_top, \
                table_distance_left, table_label in zip(
                                                        table_ids,
                                                        tables_distance_top,
                                                        tables_distance_left,
                                                        tables_label):

                table = Table(guid=str(table_id), 
                            top=table_distance_top,
                            left=table_distance_left,
                            label=table_label.strip(),
                            cafe=cafe)                    
                table.save()
            
            break
    return render(request, 'cafe/create-cafe.html')
    

def view_detail_cafe(request, pk):
    cafe = Cafe.objects.get(pk=pk)    
    tables = cafe.tables.all()
    colors = Color.objects.filter(selected=True)
    context = {'cafe': cafe, 'tables': tables, 'title': 'Detail Cafe',
                'colors': colors}
    if request.method == 'POST':
        data_dictionary = request.POST.dict()
        data_dictionary.pop('csrfmiddlewaretoken')
        #? Create new record in database for everytime saved is pressed
        print(Fore.BLUE + str(data_dictionary))
        for table_id, table_color in data_dictionary.items():
            table = cafe.tables.get(guid=str(table_id))
            old_color = table.color
            # Save new color
            table.color = table_color
            table.save()

            #? Only save record when the color field of a table changes
            if old_color != table_color:
                allocated = True
                if table_color == 'unselected-color':
                    allocated = False

                record = Record(date_time=timezone.now(),
                                table=table, allocated=allocated)
                record.save()

        messages.add_message(request, level=messages.INFO, message="Cafe saved!")
        
    return render(request, "cafe/detail-cafe.html", context=context)


def view_home(request):
    cafes = Cafe.objects.all()
    context = {'cafes': cafes, 'title': 'Home'}
    return render(request, "cafe/list-cafe.html", context=context)


@login_required
def view_delete_cafe(request, pk):
    if not request.user.is_staff:
        messages.add_message(request, level=messages.ERROR, message="You don't have permission to delete!")
        return redirect('home')
    if request.method == "POST":
        cafe = Cafe.objects.get(pk=pk)   
        print(Fore.BLUE + str(cafe)) 
        cafe.delete()
        return redirect('home')
    cafe = Cafe.objects.get(pk=pk)
    return render(request, 'cafe/delete-cafe.html', context={'cafe': cafe})


@login_required
def view_update_cafe(request, pk):
    if request.method == "POST":
        if request.FILES:

            image = request.FILES.get('image')

            #? Creating Cafe object
            cafe = Cafe.objects.get(pk=pk)
            cafe.image = image
            cafe.save()

        for i in list(request):
            #? Get tables positions and information from JSON
            data = json.loads(i)
            table_ids = list(data['table_ids'])
            tables_distance_top = list(data['array_distance_top'])
            tables_distance_left = list(data['array_distance_left'])
            tables_label = list(data['array_labels'])
            # tables_numbers = list(range(len(tables_label)))
            cafe_name = data['cafe_name']
            print(Fore.BLUE + str(data)) 


            cafe = Cafe.objects.get(pk=pk)
            cafe.name = cafe_name
            cafe.save()

            for table_id, table_distance_top, \
                table_distance_left, table_label in zip(
                                                    table_ids,
                                                    tables_distance_top,
                                                    tables_distance_left,
                                                    tables_label):
                try:
                    table = cafe.tables.get(guid=str(table_id))

                    table.top = table_distance_top
                    table.left = table_distance_left
                    table.label = table_label.strip()
                    
                except:
                    table = Table(guid=str(table_id), top=table_distance_top, left=table_distance_left,
                            label=table_label.strip(), cafe=cafe)

                table.save()
            #? Delete tables from update page 
            tables_in_database = cafe.tables.all()
            for table in tables_in_database:
                if not str(table.guid) in table_ids:
                    table.delete()
            break

    cafe = Cafe.objects.get(pk=pk)    
    tables = cafe.tables.all()
    context = {'cafe': cafe, 'tables': tables, 'title': 'Detail Cafe'}

    return render(request, 'cafe/update-cafe.html', context=context)
    

@login_required
def view_color_picklist(request):
    colors = Color.objects.all()
    if request.method == "POST":
        colors_selected = request.POST.getlist('colors')
        print(Fore.BLUE + str(colors_selected))
        for color in colors:
            #? Only Selected colors must show on the navbar
            if color.name in colors_selected:
                color.selected = True
            else:
                color.selected = False
            color.save()

    context = {'colors': colors}
    return render(request, 'color-picklist.html', context=context)


@login_required
def view_delete_table(request):
    if request.method == 'POST':
        for i in list(request):
            #? Get table number and cafe name and information from JSON
            data = json.loads(i)
            cafe_name = data['cafe_name']
            table_number = data['table_number']
            print(Fore.BLUE + "Cafe name" + str(cafe_name) + 'table number' + str(table_number))
            table = Table.objects.get(table_number=table_number, cafe__name=cafe_name)
            table.delete()
        return json.dumps(True)



@login_required
def view_admin_board(request):
    if request.method == "POST":

        messages.add_message(request, level=messages.INFO, 
                            message="Csv file generated successfully!")
    return render(request, 'download-data.html')



def create_label_column(series):
    if type(series['table']) in [float, int]:
        table = Table.objects.get(id=int(series['table']))
        return str( table.label ) 
    return series['table'].split()[1].split('=')[1].strip()


def create_cafe_column(series):
    if type(series['table']) in [float, int]:
        table = Table.objects.get(id=int(series['table']))
        return str( table.cafe ) 
    return series['table'].split()[0].split('=')[1].strip()


def generate_csv_file(request):
    NAN_REPLACE = 'Nothing'

    dataframe = pd.read_sql("SELECT * FROM cafe_record", connection, index_col='id')

    print(Fore.BLUE + str(dataframe))

    dataframe['table_id'].fillna(NAN_REPLACE, inplace=True)

    dataframe['table'] = dataframe[['table_id', 'deleted_table']].apply(lambda x: x['table_id']
                                                                            if (x['table_id'] != NAN_REPLACE)
                                                                            else x['deleted_table'], axis=1)
   
    dataframe['cafe'] = dataframe.apply(lambda x:   create_cafe_column(x),
                                                    axis=1)
    

    dataframe['label'] = dataframe.apply(lambda x:   create_label_column(x),
                                                    axis=1)

    # dataframe['label'] = dataframe.apply(lambda x:   str( Record.objects.get(id=int(x['table'])).label ) 
    #                                                 if type(x['table']) in [float, int]
    #                                                 else x['table'].split()[1].split('=')[1].strip(),
    #                                                 axis=1)
        
    dataframe.drop(columns=['table_id', 'deleted_table', 'table'], inplace=True)

    dataframe.rename(columns={'label': 'table'}, inplace=True)

    print(Fore.BLUE + str(dataframe))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=filename.csv'
    dataframe.to_csv(path_or_buf=response, float_format='%.2f', index=False,)

    return response

