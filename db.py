"""
Author : Mohamed Safarulla
Date : 06/30/2020
Description : PkMS db connection.
Licence : Open Source FSF.
Version : 1.000
"""



import pyodbc
import datetime as dt

class DB:
    def __init__(self, config, autocommit=True): #config object should be as per the Config class from config module. 
        self.time = ''
        self.autocommit = autocommit
        self.where = config.conn_string
        self.user = config.user
        self.conn = self.get_conn()
        self.cursor = self.conn.cursor()
        self.job = self.current_job()
        self.env = ''
        self.troubleshoot = False


    def get_conn(self):
        current_date = dt.datetime.now().strftime('%m%d')
        current_time = dt.datetime.now().strftime('%H%M')
        conn = pyodbc.connect(self.where, autocommit=self.autocommit)

        self.time = current_date + '@' + current_time
        return conn

    def createTemp(self, t, rl=150, l='QTEMP'):
        self.dropTemp(t)
        self.run_command(f'CRTPF FILE({l}/{t}) RCDLEN({rl})')

    def dropTemp(self, t, l='QTEMP'):
        query = """drop table %s.%s""" % (l, t)
        try:
            self.runquery(query)
        except:
            pass

    def runquery(self, query):
        query = query.replace('\\', '/')
        try:
            self.cursor.execute(query)
        except pyodbc.OperationalError:
            self.rollback()
            self.reestablish()
            raise Exception("Connection closed. Rollback issued though not needed.")

    def set_trasaction(self, autocommit):
        self.transactions = autocommit
        self.conn.autocommit = self.autocommit

    def read_all(self, query) -> object:
        try:
            ret = self.cursor.execute(query)
        except pyodbc.OperationalError as e:
            self.reestablish()
            ret = self.cursor.execute(query)
        return ret

    def read_one(self, query):
        try:
            self.cursor.execute(query)
        except pyodbc.OperationalError as e:
            self.reestablish()
            self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return row

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def getQuestionMarks(self, num):  # irrelevant function just to format the insert query with ?,?,?,.....
        return ','.join(list('?' * num))

    def insert_rows(self, query, rows):
        if type(rows) != list:
            rows = [rows]
        query = query + ' values (%s)'
        query = query % self.getQuestionMarks(len(rows[0].cursor_description))
        self.cursor.fast_executemany = True
        self.cursor.executemany(query, rows)

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        del self.conn
        del self.cursor
        self.job = 'connection closed'

    def reestablish(self):
        self.conn = self.get_conn()
        self.cursor = self.conn.cursor()
        self.job = self.current_job()

    def run_command(self, command):
        command = "call qcmdexc('%s')" % command
        try:
            self.cursor.execute(command)
        except pyodbc.OperationalError:
            self.reestablish()
            self.cursor.execute(command)
        except AttributeError:
            self.reestablish()

    def se(self, env):
        self.env = env.upper()
        try:
            self.run_command('ADDLIBLE PKTOOL')
        except:
            pass
        self.run_command('se %s' % env)

    def debug(self):
        if not self.troubleshoot:
            self.run_command('STRDBG UPDPROD(*YES)')
            self.troubleshoot = True
            print("DEBUG ON")
        else:
            self.run_command('ENDDBG')
            self.troubleshoot = False
            print("DEBUG OFF")

    def current_job(self):  # dont call this directly.
        self.dropTemp('TEST')
        self.run_command('WRKJOB OUTPUT(*PRINT) OPTION(*RUNA)')
        self.run_command('CRTPF FILE(QTEMP/TEST) RCDLEN(200)')
        self.run_command(f'CPYSPLF FILE(QPDSPJOB) TOFILE(QTEMP/TEST) JOB({self.user}/QPRTJOB) SPLNBR(*LAST)')
        row = self.read_one('select * from QTEMP.TEST a where rrn(a)=2  ')
        job = row.TEST[15:25].strip()
        user = row.TEST[43:53].strip()
        number = row.TEST[76:86].strip()
        return '%s/%s/%s' % (number, user, job)

    def endjob(self, j):
        cmd = 'sbmjob cmd(ENDJOB %s OPTION(*IMMED) DELAY(1))' % (self.job if not j else j)
        self.run_command(cmd)
