#!/usr/bin/env python
# -*- coding: utf-8 -*-
#jackey0003@hotmail.com
#利用mysql binlog实现dml语句的监控,自动生成回滚语句,协助分析问题操作
import yaml
from analysis import *
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import (
    QueryEvent, RotateEvent, FormatDescriptionEvent,
    XidEvent, GtidEvent, StopEvent,
    BeginLoadQueryEvent, ExecuteLoadQueryEvent,
    HeartbeatLogEvent, NotImplementedEvent)
from pymysqlreplication.row_event import (
    UpdateRowsEvent, WriteRowsEvent, DeleteRowsEvent, TableMapEvent)

class flashbackup(object):
    def __init__(self,conf='conf.yaml'):
        self.f = open(conf)
        self.dataMap = yaml.load(self.f)
        self.f.close()

    def writeLog(self,file,msg):
        f = file
        file_object = open(f, 'a')
        try:
            file_object.write(msg)
        finally:
            file_object.close()

    def get_conf(self):
        res = {}
        SETTINGS = self.dataMap['SETTINGS']
        server_conf = SETTINGS['server_conf']
        for set in server_conf:
            myset = SETTINGS[server_conf[set]]
            if myset['is_set'] == 1:
                res['tables'] = myset['tables']
                res['passwd'] = myset['passwd']
                res['log_pos'] = myset['log_pos']
                res['host'] = myset['host']
                res['user'] = myset['user']
                res['log_file'] = myset['log_file']
                res['port'] = myset['port']
                res['schemas'] = myset['schemas']
            else:
                pass
        res['log'] = SETTINGS['log']
        res['server_id'] = SETTINGS['server_id']
        return res

    def run_repl(self):
        res = self.get_conf()
        self.host = res['host']
        self.port = res['port']
        self.user = res['user']
        self.passwd = res['passwd']
        self.log_file = res['log_file']
        self.log_pos = res['log_pos']
        self.schemas = res['schemas']
        self.tables = res['tables']
        self.server_id = res['server_id']
        #print self.RowsEvent
        MYSQL_SETTINGS = {"host":self.host,"port":self.port,"user":self.user,"passwd":self.passwd }
        stream = BinLogStreamReader(connection_settings=MYSQL_SETTINGS, resume_stream=True,
                    log_pos=self.log_pos, log_file=self.log_file,
                    server_id=self.server_id, only_events=(DeleteRowsEvent,UpdateRowsEvent,WriteRowsEvent),
                    fail_on_table_metadata_unavailable=True, freeze_schema=True,
                    #only_schemas=(self.schemas),
                    #only_tables=(self.tables),
                    blocking=True)
        log_pos_list = []
        for binlogevent in stream:
            log_pos_list.append(binlogevent.packet.log_pos)
            if len(log_pos_list) <=1 :
                log_pos = 0
            else:
                log_pos = log_pos_list[0]
                del log_pos_list[0]
            #log_pos = binlogevent.packet.log_pos
            rows = binlogevent.rows
            table = binlogevent.table
            event_type=binlogevent.event_type
            log_level = res['log']['log_level']
            analysis_ = analysis(table,event_type,rows,log_pos,log_level)
            analysis_res = analysis_.run_all_analysis()
            for i in analysis_res:
                print i
        stream.close()

if __name__ == "__main__":
    tt = flashbackup('conf.yaml')
    tt.run_repl()


