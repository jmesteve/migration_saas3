import os
import shutil
import psycopg2 as dbapi2

DIR_POSTGRESQL = '/Applications/Postgres.app/Contents/MacOS/bin/'
HOST = 'localhost'
USER = 'openerp'
DATABASE = 'postgres'

def backup(list_directory):
    pg_dump = DIR_POSTGRESQL + 'pg_dump' 
    destination_dir = '' 
    for database in list_directory:
        destination_path = destination_dir + database
        try:
            shutil.rmtree(destination_path)
        except:
            print "no remove" 
              
        try:
            os.system('%s -U %s %s -F d --inserts --column-inserts -f %s'%(pg_dump,USER,database,destination_path))
            print "backup_successfull"
        except:
            print "backup unsuccessfull"

def backup_plain(list_directory):
    pg_dump = DIR_POSTGRESQL + 'pg_dump' 
    destination_dir = '' 
    for database in list_directory:
        destination_path = destination_dir + database + "/" + "schema.dump"
        try:
            shutil.rmtree(destination_path)
        except:
            print "no remove" 
              
        try:
            os.system('%s -U %s %s -F p -s -f %s'%(pg_dump,USER,database,destination_path))
            print "backup_plain_successfull"
        except:
            print "backup plain unsuccessfull"      
            
def restore(source_directory,destination_directory):
    pg_restore = DIR_POSTGRESQL + 'pg_restore' 
    iter = 0
    try:
        for database in destination_directory:
            destination_path = source_directory[iter]
            iter += 1
            os.system('%s -d %s %s'%(pg_restore,database,destination_path))
        print "restore successfull"
    except:
        print "restore unsuccessfull"   
            
def create(list_directory):
    chosen_template = 'template1'
    for database in list_directory:
        try:
            connection="dbname=%s user=%s host=%s password=''"%(DATABASE,USER,HOST)
            conn = dbapi2.connect(connection)
            conn.set_isolation_level(dbapi2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cr = conn.cursor()
            cr.execute("SELECT datname FROM pg_database WHERE datname = %s",
                           (database,))
            if cr.fetchall():
                cr.execute('DROP DATABASE "%s"' % database)
            
            cr.execute("""CREATE DATABASE "%s" ENCODING 'unicode' TEMPLATE "%s" """ % (database, chosen_template)) 
            print "create successfull"
           
        except:
            print "create  unsuccessfull"
            
        finally:
            if conn:
                conn.close()
                
def drop(list_directory):
    chosen_template = 'template1'
    for database in list_directory:
        try:
            connection="dbname=%s user=%s host=%s password=''"%(DATABASE,USER,HOST)
            conn = dbapi2.connect(connection)
            conn.set_isolation_level(dbapi2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cr = conn.cursor()
            cr.execute("SELECT datname FROM pg_database WHERE datname = %s",
                           (database,))
            if cr.fetchall():
                cr.execute('DROP DATABASE "%s"' % database)
            
            print "drop successfull"
           
        except:
            print "drop unsuccessfull"
            
        finally:
            if conn:
                conn.close()
                
def list():
    try:
        connection="dbname=%s user=%s host=%s password=''"%(DATABASE,USER,HOST)
        conn = dbapi2.connect(connection)
        cr = conn.cursor()
        cr.execute("SELECT datname FROM pg_database")
        list = []
        databases =  cr.fetchall()
        for database in databases:
            list.append(database[0])
        return list
            
    except:
        print "list unsuccessfull"   
    finally:
        if conn:
            conn.close()

def listTables(database):
    try:
        connection = ("dbname=%s user=%s host=%s password=''"%(database,USER,HOST))
        conn = dbapi2.connect(connection)
        cr = conn.cursor()
        cr.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_type='BASE TABLE';")
        list = []
        tables =  cr.fetchall()
        for table in tables:
            list.append(table[0])
        list.sort()
        return list
            
    except:
        print "list tables unsuccessfull"   
    finally:
        if conn:
            conn.close()
            
