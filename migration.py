import shutil
from os import listdir, path, makedirs, remove

def create2(source, destination, source_directory, destination_directory):
    extension = '.dat'
    try:
        len_source = len(source)
        len_dest = len(destination)
        
        if len_source == len_dest:
            for i in range(len_source):
                path_source = source_directory+ str(source[i]) + extension
                path_destination = destination_directory + str(destination[i]) + extension
                path_tmp = 'tmp/' + str(destination[i]) + extension
                shutil.copy(path_destination, path_tmp)
                shutil.copy(path_source, path_destination)
        print "migration successfull" 
    except:
        print "migration unsuccessfull"     
            

def create(source_directory, destination_directory):
    tableContent = 'table_content'
    extension = '.dat'
    path_change = tableContent +"_" + source_directory[0] + extension
    try:
        dir_destination = destination_directory[0]+ "/" 
        file_destination = dir_destination + tableContent + extension
        dir_source = source_directory[0] + "/" 
        file_source = dir_source + tableContent + extension
        dir_tmp = 'tmp/'
        try:
            shutil.rmtree(dir_tmp)
        except:
            print "tmp remove failure"
        
        if not path.exists(dir_tmp):
            makedirs(dir_tmp)
        
        fsource = open(file_source)
        dataSource = fsource.read() 
        dataSource = dataSource.split("\n")
        dictSource = {}
        dict={}
        if dataSource:
            for line in dataSource:
                line = line.split()
                try:
                    dictSource[line[3]]=line[0]
                    dict[line[0]]=line[3]
                except:
                    print "no content"
        fsource.close()
        
        fchange = open(path_change)  
        dataChange = fchange.read() 
        dataChange = dataChange.split("\n")
        dictChange = {}
        if dataChange:
            for line in dataChange:
                line = line.split()
                try:
                    dictChange[line[0]]=True
                except:
                    print "no content"
        fchange.close()
           
        f = open(file_destination)
        data = f.read()
        data = data.split("\n")
        f.close()
        
        dictDest = {}
        if data:
            for line in data:
                try:
                    line = line.split()
                    dictDest[line[3]]=line[0]
                    if dictChange.has_key(line[3]):
                        field0_source = str(dictSource[line[3]])
                        path_source = dir_source + field0_source + extension
                        path_tmp = dir_tmp + str(line[0]) +extension
                        shutil.copy(path_source,path_tmp)
                    #if line[1]=='e':
                    #    field0_source = str(dictSource[line[3]])
                    #    path_source = dir_source + field0_source + extension
                    #    path_tmp = dir_tmp + str(line[0]) +extension
                    #    shutil.copy(path_source,path_tmp)
                    #elif line[1]=='t':
                    #    field0_t = str(line[2])
                    #    path_source = dir_source + field0_t + extension
                    #    path_tmp_t = dir_tmp + str(line[0]) +extension
                    #    shutil.copy(path_source,path_tmp_t)
                    else:
                        field0 = str(line[0])
                        path_destination = dir_destination + field0 +extension
                        path_tmp = dir_tmp + field0 +extension
                        shutil.copy(path_destination,path_tmp)
                except:
                    print "not a number"
            shutil.copy(dir_destination + 'toc.dat',dir_tmp + 'toc.dat')
            dir_exception = source_directory[0] + "_exception/"
            list = listdir(dir_exception)
            for line in list:
                file, extension = path.splitext(line)
                file_dest = str(dictDest[file]) + extension
                path_dest = dir_tmp + file_dest 
                path_exception = dir_exception + line
                remove(path_dest)
                shutil.copy(path_exception,path_dest)
        
        print "migration successfull" 
    except:
        print "migration unsuccessfull"    

        
def empty(source_directory, destination_directory):
    tableContent = 'table_content'
    extension = '.dat'
    try:
        file_source = source_directory[0] + "/" + tableContent + extension
        dir_destination = destination_directory[0]+ "/" 
        dir_source = source_directory[0] + "/" 
        if not path.exists(dir_destination):
            makedirs(dir_destination)
              
        f = open(file_source)
        data = f.read()
        
        
        if data:
            for line in data.split('\n'):
                try:
                    file = line.split(' ',1)
                    field0 = str(file[0])
                    path_destination = dir_destination + field0 +extension
                    path_source = dir_source + field0 +extension
                    field1 = file[1][0]
                    if field1 =='e':
                        open(path_destination, 'a').close()   
                    else:
                        shutil.copy(path_source,path_destination)
                except:
                    print "not a number"
            shutil.copy(dir_source + 'toc.dat',dir_destination + 'toc.dat')
           
        
        print "migration empty successfull" 
    except:
        print "migration empty unsuccessfull"    