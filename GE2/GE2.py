'''
    @author: 
    @email: 
    @created: 
    @modified: 
    @desc: 
'''
import sys
from mysql import connector
from mysql.connector import errorcode
from constants import *


class Biosequence:
    def __init__(self, Type, Sequence, Creator):
        self.Type = Type
        self.Sequence= Sequence.upper()
        self.Creator = Creator

    def validate_sequence(self, Sequence):
        RNAset = set(RNA_Bases)
        DNAset = set(DNA_Bases)
        COMMONset = set(COMMON_Bases)
        bioseqset = set(Sequence.upper())
        if bioseqset.issubset(COMMONset):
            print("Valid RNA/DNA seq ... only common bases ...")
            return (True, 'COMMON')
        else:
            if bioseqset.issubset(RNAset):
                print("seq is RNA seq")
                return (True, 'RNA')
            else:
                print("Not a valid RNA seq ... continue ...({})".format(len(bioseqset - RNAset)))
            if bioseqset.issubset(DNAset):
                print("seq is DNA seq")
                return (True, 'DNA')
            else:
                print("Not a valid DNA seq ... continue ...({})".format(len(bioseqset - RNAset)))
                return (False, 'NotValid')

    def get_Sequence(self):
        return self.Sequence


    def get_Type(self):
        return self.Type

    def set_Type(self, new_type):
        self.Type = new_type
        return self.Type

    def print_info(self, dbid = -1):
        if dbid != -1:
            print("========== For DB ID {} rec ==========".format(dbid))
        else:
            print("========================================")
        print("          Type:     {}".format(self.Type))
        print("          Sequence: {}".format(self.Sequence))
        print("          Creator:  {}".format(self.Creator))
        print("========================================")

def display_menu():
    print("\n========================================")
    for key in menu_options.keys():
        print ("    {}) {}".format(key, menu_options[key]))
    print("========================================\n")

def insert_db_entry(dbconn, table_name, s):
    print("Insert New Entry ...")
    cursor = dbconn.cursor(buffered=True)
    sql_cmd = "INSERT INTO {} (Seq_Type, Seq_Val, Creator) VALUES (%s, %s, %s)".format(table_name)
    print("Type is {}".format(s.Type))
    print("Sequence is {}".format(s.Sequence))
    val = []
    val.append("{}".format(s.Type))
    val.append("{}".format(s.Sequence))
    val.append("{}".format(s.Creator))

    cursor.execute(sql_cmd, val)
    dbconn.commit()


def get_id_input():
    while True:
        try:
            prompt = "Enter id for entry to be retrieved: "
            iid = int(input(prompt))
            if  iid > 0:
                print("Entry Id to be retrieved for del/print: {}".format(iid))
                break
            else:
                print("entry should be a positive number")
        except ValueError:
            print("Please enter a valid integer > 0 ")
    return iid

def retrieve_db_id(dbconn, table_name, dbid):
    print("Retrieve Entry ID ...")
    count = 0
    try:
        cursor = dbconn.cursor(buffered=True)
        sql_cmd = "SELECT count(*) FROM {} WHERE ID = {}".format(table_name, dbid)
        cursor.execute(sql_cmd)
        # quirky use of fetchone or we get a python error
        count, = cursor.fetchone()
        print("record(s) found: {}".format(count))
        if count > 0:
             print("Found {} record(s)".format(count))
        else:
             print("No record(s) found ")
        #dbconn.commit()
    except connector.Error as err:
        print("Error Code: {} count: {}".format(err.errno, count))
    return count

def retrieve_db_entry(dbconn, table_name, id):
    print("Retrieve Entry ...")
    try:
        cursor = dbconn.cursor(buffered=True)
        sql_cmd = "SELECT * FROM {} WHERE ID = {}".format(table_name, id)
        cursor.execute(sql_cmd)
        res = list(cursor.fetchall())
    except connector.Error as err:
        print("Error Code: {}".format(err.errno))
        print("SQLSTATE {}".format(err.sqlstate))
        print("Message {}".format(err.msg))
    return res, len(res)

def delete_db_entry(dbconn, table_name, id):
    print("Delete Entry ... with ID: {}".format(id))
    try:
        cursor = dbconn.cursor(buffered=True)
        sql_cmd = "DELETE FROM {} WHERE ID = {}".format(table_name, id)
        cursor.execute(sql_cmd)
        print("record(s) deleted: {}".format(cursor.rowcount))
    except connector.Error as err:
        print("Error Code: {}".format(err.errno))
        print("SQLSTATE {}".format(err.sqlstate))
        print("Message {}".format(err.msg))
    dbconn.commit()



def initialize_db():
    try:
        dbconn = connector.connect(
           host= HOST,
           user= USER,
           password= PASSWORD)
        print("Connection established: {}".format(dbconn))
    except connector.Error as err:
        print(err)
    return dbconn

def check_db_existence(dbconn, db_name):
    # get  a cursor object
    status=False
    cursor = dbconn.cursor(buffered=True)
    sql_cmd = "CREATE DATABASE IF NOT EXISTS {};".format(db_name)
    #sql_cmd = "SHOW DATABASES"
    print("checking existence and create if not there")
    try:
        cursor.execute(sql_cmd)
    except connector.Error as err:
        print("Error {} when checking db {} existence".format(err.msg, db_name))
        return status
    cursor.close()
    cursor = dbconn.cursor(buffered=True)
    try:
        sql_cmd = "use {};".format(db_name)
        cursor.execute(sql_cmd)
        status=True
    except connector.Error as err:
        print("cannot use db {} error {}".format(db_name, err.msg))
    cursor.close()
    return status


def create_db_Table(dbconn, db_table):
    status=False
    # get  a cursor object
    cursor = dbconn.cursor()
    sql_cmd = "CREATE TABLE {} (ID INT AUTO_INCREMENT PRIMARY KEY, Seq_Type varchar(3) NOT NULL, Seq_Val varchar(1024) NOT NULL, Creator varchar(100) NOT NULL, CONSTRAINT chk_Type CHECK (Seq_Type IN ('RNA', 'DNA')));".format(db_table)
    try:
        cursor.execute(sql_cmd)
    except connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.\n")
            status=True
        else:
            print("Error in checking for table {}".format(err.msg))
            return status
    cursor.close()
    return status


def get_BioSeqType(intype):
    if intype == 1:
        return 'RNA'
    elif intype == 2:
        return 'DNA'
    else:
        return 'INVALID'


def get_entry_data():
    objNotValid = True
    while objNotValid:
        while True:
            try:
                prompt = "Enter bio sequence (up to 1024 chars): "
                bioseq = input(prompt)
                if bioseq.isalpha():
                    if len(bioseq) > MAX_LEN:
                        print("Max len of sequence should be less than {}".format(MAX_LEN))
                    else:
                        print("valid seq data ...")
                        bioseq = bioseq.upper()
                        break
            except TypeError:
                 print('Use only letters for the sequence string ...')

        prompt = "Enter bio sequence type (either 1=RNA or 2=DNA): "
        while True:
             try:
                ntype = int(input(prompt))
                if  0 < ntype < 3:
                    seqtype = get_BioSeqType(ntype)
                    print("You have selected: {}".format(seqtype))
                    break
                else:
                    print("selected entry should be in [1, 2]")
             except ValueError:
                print("Please enter a valid integer 1 or 2")

        prompt = "Enter bio sequence creator: "
        while True:
            try:
                creator = input(prompt)
                if len(creator) > MAX_CR_LEN:
                    print("Max len of creator name should be less than {}".format(MAX_CR_LEN))
                else:
                    break
            except TypeError:
                print("Please enter a char string for creator")

        bioseq_obj = Biosequence(seqtype, bioseq, creator)
        # print("entered sequence is {}".format(bioseq_obj.get_Sequence()))
        (val_result, val_type) = bioseq_obj.validate_sequence(bioseq_obj.get_Sequence())
        # print("validation type is {}".format(val_type))
        if val_result:
            if val_type == "COMMON":
                print("Let user to decide only common bases are contained ...selected Object is valid")
                objNotValid = False  # New object validated
            else:
                if val_type != bioseq_obj.get_Type():
                    print("Incompatible Types: Type from Validation {} while Type selected : {}".format(val_type, bioseq_obj.get_Type()))
                else:
                    print("Type is correctly selected Object is valid")
                    objNotValid = False
        else:
            print("seq contains invalid chars not RNA or DNA please try again")
    return bioseq_obj



if __name__=='__main__':

   print("some necessary Initializations ...")
   print("starting ...")

   mydbconn = initialize_db()
   if not check_db_existence(mydbconn, DB_NAME):
       sys.exit(1)
   if not create_db_Table(mydbconn, TABLE):
       sys.exit(1)

   while(True):
        display_menu()
        opt = ""
        try:
            opt = int(input('Enter your option: '))
        except:
            print('Wrong input. Please enter a number')
        if opt == 1:
           print("Inserting new entry... ")
           print("getting & validating new data ...")
           # create the object
           s = get_entry_data()
           s.print_info()
           insert_db_entry(mydbconn, TABLE, s)
        elif opt == 2:
            iid = get_id_input()
            entry_count = retrieve_db_id(mydbconn, TABLE, iid)
            if entry_count > 0:
                print("About to delete {} entries".format(entry_count))
                delete_db_entry(mydbconn, TABLE, iid)
            else:
                print("Nothing to delete No entry found in db with id {}".format(iid))

        elif opt == 3:
            id = get_id_input()
            entry_list, list_size = retrieve_db_entry(mydbconn, TABLE, id)
            if list_size == 1:
                print("One entry found {}".format(entry_list))
                s = Biosequence(entry_list[0][1], entry_list[0][2], entry_list[0][3])
                s.print_info(id)
            else:
                print("Found {} objects - or something went wrong".format(list_size))

        elif opt == 4:
            print('Thank you for using the application')
            sys.exit(0)
        else:
            print('Invalid option. Please enter a number between 1..4')

