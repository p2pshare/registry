# Add Share
# Search Share

# files:
#   file_id INTEGER PRIMARY KEY,
#   filename TEXT,
#   hash TEXT,
#   author TEXT
#   chunk_info TEXT,
#
# files_trackers:
#   files_trackers_id INTEGER PRIMARY KEY,
#   file_id INTEGER,
#   tracker TEXT,
#   FOREIGN KEY(file_id) REFERENCES files(file_id)
#


import sqlite3
import hashlib
import json
def justBuildTableIfNonexistence(tablename):
    connection = sqlite3.connect("share.db")
    connection.isolation_level = None
    cursor = connection.cursor()
    tablename = tablename.strip().upper()
    sql_statement = "SELECT name FROM sqlite_master WHERE type='table' AND name='"+tablename+"';"
    print "Going to test if the table '"+tablename+"' exists?"
    if sqlite3.complete_statement(sql_statement):
        try:
            sql_statement = sql_statement.strip()
            cursor.execute(sql_statement)
            if sql_statement.lstrip().upper().startswith("SELECT"):
                if len(cursor.fetchall()) == 0:
                    print tablename+" does not exist, so now going to create one."
                    if tablename == "FILES":
                        sql_statement = "CREATE TABLE "+tablename+"( file_id INTEGER PRIMARY KEY, filename TEXT, hash TEXT, author TEXT, chunk_info TEXT);"
                    elif tablename == "FILES_TRACKERS":
                        sql_statement = "CREATE TABLE "+tablename+"( files_trackers_id INTEGER PRIMARY KEY, file_id INTEGER, tracker TEXT, FOREIGN KEY(file_id) REFERENCES files(file_id));"
                    else:
                        sql_statement = "INVALID"
                    if sql_statement != "INVALID":
                        print "Going to execute"
                        print "\t"+sql_statement
                        if sqlite3.complete_statement(sql_statement):
                            try:
                                sql_statement = sql_statement.strip()
                                connection.execute(sql_statement)
                            except sqlite3.Error as e:
                                print "An error occurred:", e.args[0]
                    else:
                        print "Table '"+tablename+"' has not been defined.\n"
                    connection.close()
                    return True
                else:
                    return False
        except sqlite3.Error as e:
             print "An error occurred:", e.args[0]
    connection.close()


# def main():
#     # str = '{ "id": 12, "filename": "filename.mp4", "hash": "{}md5hash}", "author": "{{ username }}", "chunks": [{ "id": 1, "hash": "{{hash}}" }, { "id": 2, "hash": "{{hash}}" }, { "id": 3, "hash": "{{hash}}" }, { "id": 4, "hash": "{{hash}}" }], "trackers": [ "t1.p2pshare.net", "t2.p2pshare.net", "t3.p2pshare.net", "t4.p2pshare.net" ] }'
#     # print json.loads(str)
#
#     # add("filename", "author", ["tracker1", "tracker2", "tracker3"])
#     print search("filename","filename")

# Search for a registry by filename? by hash? by author?
# type: filename or hash or author
def search(search_key, search_type):
    isFilesNew = justBuildTableIfNonexistence("FILES")
    isFiles_TrackersNew = justBuildTableIfNonexistence("FILES_TRACKERS")
    if isFilesNew is True or isFiles_TrackersNew is True:
        print "One or more of the designated tables is newly established, so no search action was done."

    if search_type is not None:
        if search_type == "filename":
            sql_statement = "SELECT * FROM FILES f WHERE f.filename = '"+search_key+"';"
        elif search_type == "hash":
            sql_statement = "SELECT * FROM FILES f WHERE f.hash = '"+search_key+"';"
        elif search_type == "author":
            sql_statement = "SELECT * FROM FILES f WHERE f.author = '"+search_key+"';"
        elif search_type == "id":
            sql_statement = "SELECT * FROM FILES f WHERE f.file_id = '"+search_key+"';"
        elif search_type == "id_trackers":
            sql_statement = "SELECT DISTINCT f.tracker FROM FILES_TRACKERS f WHERE f.file_id = '"+search_key+"';" 
        else:
            print "The Search Type '"+search_type+"' has not been defined."
            sql_statement = "INVALID"
    else:
        print "Search Type has to be stated. Please fill in the search type."
        sql_statement = "INVALID"

    if sql_statement == "INVALID":
        return None
        # pass
    else:
        connection = sqlite3.connect("share.db")
        connection.isolation_level = None
        cursor = connection.cursor()
        if sqlite3.complete_statement(sql_statement):
            try:
                sql_statement = sql_statement.strip()
                cursor.execute(sql_statement)
                if sql_statement.lstrip().upper().startswith("SELECT"):
                    return cursor.fetchall()
            except sqlite3.Error as e:
                print "An error occurred:", e.args[0]
                connection.close()
                return None
        connection.close()
        return None


def add(filename, author, *trackers):
    justBuildTableIfNonexistence("FILES")
    justBuildTableIfNonexistence("FILES_TRACKERS")

    connection = sqlite3.connect("share.db")
    connection.isolation_level = None
    cursor = connection.cursor()
    hashValue = hashlib.md5()
    hashValue.update(filename)
    hashValue.update(author)
    hash = hashValue.hexdigest()
    sql_statement = "INSERT INTO FILES(filename, hash, author, chunk_info) VALUES('"+filename+"','"+hash+"','"+author+"', '');"
    print "Going to execute()\n\t"+sql_statement
    if sqlite3.complete_statement(sql_statement):
        try:
            sql_statement = sql_statement.strip()
            cursor.execute(sql_statement)
            #Get file_id
            sql_statement = "SELECT f.file_id FROM files f WHERE hash='"+hash+"';"
            print "Going to execute()\n\t"+sql_statement
            cursor.execute(sql_statement)
            file_id = cursor.fetchone()[0]
            print type(file_id)
            for each_tracker in trackers:
                for each in each_tracker:
                    sql_statement = "INSERT INTO FILES_TRACKERS(file_id, tracker) VALUES("+str(file_id)+",'"+each+"');"
                    print "Going to execute()\n\t"+sql_statement
                    if sqlite3.complete_statement(sql_statement):
                        try:
                            sql_statement = sql_statement.strip()
                            cursor.execute(sql_statement)
                        except sqlite3.Error as e:
                            print "An error occurred:", e.args[0]
                            return None
            return file_id
        except sqlite3.Error as e:
             print "An error occurred:", e.args[0]
             connection.close()
             return None
    connection.close()
    return None
# if __name__ == "__main__":
#     main()
