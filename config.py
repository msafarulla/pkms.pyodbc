"""
Author : Mohamed Safarulla
Date : 06/30/2020
Description : PkMS db connection config class.
Licence : Open Source FSF.
Version : 1.000
"""

class Config:
    def __init__(self,ip,user,password):
        self.server_ip = ip
        self.user = user
        self.password = password
        self.conn_string = f"driver={{iSeries Access ODBC Driver}};dsn={{}};system={ip};uid={self.user};pwd={self.password};naming=1;translate=1"
