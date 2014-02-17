import os
from os import listdir, path
import database
import re

def sort_list(list,pattern):
    res = []
    for line in list:
        file, extension = path.splitext(line)
        try:
            res.append(int(file))
        except:
            print "not a number"
    res.sort() 
    new_res=[]
    for line in res:
        new_res.append(str(line)+pattern)
            
    return new_res

def schema_tables(directory):
    path_file = directory + "/schema.dump"
    f = open(path_file)
    data = f.read()
    pattern = 'CREATE TABLE'
    lenPattern = len(pattern)+1
    value=0
    list=[]
    while value!=-1:
        if value==0:
            value = -1
        value = data.find(pattern,value+1)
        begin = value + lenPattern
        end = begin + 100
        word = data[begin:end]
        list.append(word.split(' ')[0])
    return list
    
def obtain(list_directory):
    separator=" "
    pattern = '.dat'
    lenColumn = 1
    toc = 'table_content.dat'

    try:
        for directory in list_directory:
            tables = schema_tables(directory)
            #tables = database.listTables(directory)
            directory += '/'
            list = listdir(directory)
            list = sort_list(list,pattern)
            
            table_content = directory + toc
            fwrite = open(table_content, 'w')
            for line,table in zip(list,tables):
                file, extension = path.splitext(line)
                if extension == pattern:
                    path_file = directory + line
                    f = open(path_file)
                    data = f.read()
                    if data:
                        separator=" "
                        first_line = data.split('\n', 1)[0]
                        columns = first_line.split(separator)
                        count_lines = str(len(data.split('\n')))
                        lenColumnTotal = lenColumn + 5 - len(count_lines)
                        if len(columns)>2:
                            if columns[2]==table:
                                row =  file +' = ' +count_lines+ ' '*lenColumnTotal +columns[2] + '\n'
                            else:
                                row =  file +' x ' +count_lines+ ' '*lenColumnTotal +columns[2] + '\n'
                            fwrite.write(row)
                        else:
                            row = file +' ? ' + '0' + ' '*lenColumnTotal + table + '\n'
                            fwrite.write(row)
                    f.close();
            fwrite.close()
        print ('table content successfull')
    except:
        print "table content unsuccessfull"    
        
        
def compare(list_directory):
    toc = 'table_content.dat'
    separator = '\n'
    res = []
    max_lines = 0
    lenColumn = 0
    
    try:
        for directory in list_directory:
            directory += '/'
            file_path = directory + toc
            count = len(open(file_path).readlines())
            if max_lines < count:
                max_lines = count
                
        for index in range(max_lines):
            res.append('')
        
        for directory in list_directory:
            directory += '/'
            file_path = directory + toc
            index = 0
            for line in open(file_path):        
                columns = line.split(separator)
                if len(line)>lenColumn:
                    lenColumn = len(line) 
                if len(columns) > 0:
                    if len(res[index])==0:
                        res[index] = [columns[0]]
                    else:
                        res[index] += [columns[0]]
                    index += 1
            if index<max_lines:
                for i in range(index,max_lines):
                    res[i] = ['']
        
        fwrite = open(toc, 'w')
        for line in res:
            len_line = len(line)
            row = ''
            for i in range(len_line):
                lenCol = lenColumn - len(line[i]) 
                row += line[i] + ' '*lenCol
            row += '\n'
            fwrite.write(row)
        fwrite.close()    
        print "table content compare successfull" 
    except:
        print "table content compare unsuccessfull"     
       