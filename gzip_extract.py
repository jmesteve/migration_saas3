import gzip
import os
from os import listdir, path

def extract(list_directory):
    pattern = '.gz'
    separator=" "
    
    try:   
        for directory in list_directory:
            directory += '/'
            list = listdir(directory)
            for line in list:
                file, extension = path.splitext(line)
                if extension == pattern:
                    path_file = directory + line
                    inF = gzip.GzipFile(path_file,'rb')
                    f = inF.read()
                    inF.close()
                    
                    path_file_out = str(directory + file)
                    outF = open(path_file_out, 'w')
                    outF.write(f)
                    outF.close()
                    
                    os.remove(path_file)
        print "gzip successfull" 
    except:
        print "gzip unsuccessfull"     
            


