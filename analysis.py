#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 语句分析类
import datetime
import decimal
class analysis(object):
    def __init__(self,table,event_type,rows,log_pos,log_level):
        self.table = table
        self.event_type = event_type
        self.row = rows
        self.log_pos = log_pos
        self.log_level = log_level

    def insert_format(self,table, dic):
        result = []
        for dic_ in dic:
            keys = dic_['values'].keys()
            values = dic_['values'].values()
            p_k = ''
            for k in keys:
                p_k = p_k + "`%s`" % k + ","
            p_k = p_k[:-1]
            p_v = ''
            for v in values:
                if type(v) == type(1):
                    p_v = p_v + "%d" % v + ","
                if type(v) == type(u'a'):
                    vl = v
                    p_v = p_v + "'%s'" % vl + ","
                if type(v) == type(datetime.datetime.now()):
                    vl = v
                    p_v = p_v + "'%s'" % vl + ","
                    # print type(before_values[p])
                if type(v) == type(decimal.Decimal(1.1)):
                    vl = v
                    p_v = p_v + "'%s'" % vl + ","
            p_v = p_v[:-1]
            p = {'key': p_k, 'value': p_v}
            sql = "insert into %s (%s) value (%s)" % (table, p['key'], p['value'])
            result.append(sql)
        return result

    def delete_format(self,table, dic):
        result = []
        for dic_ in dic:
            value = dic_['values']
            keys = value.keys()
            p_k_v = ''
            for p in keys:
                if type(value[p]) == type(1):
                    p_k_v = p_k_v + "`%s`=%d and " % (p, value[p])
                if type(value[p]) == type(u'a'):
                    vl = value[p]
                    p_k_v = p_k_v + u"`%s`='%s' and " % (p, vl)
                if type(value[p]) == type(datetime.datetime.now()):
                    vl = value[p]
                    p_k_v = p_k_v + "`%s`='%s' and " % (p, str(vl))
                    # print type(before_values[p])
                if type(value[p]) == type(decimal.Decimal(1.1)):
                    vl = value[p]
                    p_k_v = p_k_v + "`%s`='%f' and " % (p, vl)
            p_k_v = p_k_v[:-4]
            sql = u"delete from %s where %s " % (table, p_k_v)
            result.append(sql)
        return result

    def update_format(self,table, dic, ty):
        result = []
        for dic_ in dic:
            value = dic_
            before_values = value['before_values']
            after_values = value['after_values']
            keys_b = before_values.keys()
            p_k_v_b = ''
            if ty == 'dml':
                for p in keys_b:
                    if type(before_values[p]) == type(1):
                        p_k_v_b = p_k_v_b + "`%s`=%d and " % (p, before_values[p])
                    if type(before_values[p]) == type(u'a'):
                        vl = before_values[p]
                        p_k_v_b = p_k_v_b + "`%s`='%s' and " % (p, vl)
                    if type(before_values[p]) == type(datetime.datetime.now()):
                        vl = before_values[p]
                        p_k_v_b = p_k_v_b + "`%s`='%s' and " % (p, str(vl))
                    #print type(before_values[p])
                    if type(before_values[p]) == type(decimal.Decimal(1.1)):
                        vl = before_values[p]
                        p_k_v_b = p_k_v_b + "`%s`='%f' and " % (p, vl)
                p_k_v_b = p_k_v_b[:-4]
                keys_a = after_values.keys()
                p_k_v_a = ''
                for p in keys_a:
                    if type(after_values[p]) == type(1):
                        p_k_v_a = p_k_v_a + "`%s`=%d ," % (p, after_values[p])
                    if type(after_values[p]) == type(u'a'):
                        vl = after_values[p]
                        p_k_v_a = p_k_v_a + "`%s`='%s'," % (p, vl)
                p_k_v_a = p_k_v_a[:-1]
                p = {'before': p_k_v_b, 'after': p_k_v_a}
                sql = "update %s set %s where %s" % (table, p['before'], p['after'])
                result.append(sql)
            else:
                for p in keys_b:
                    if type(before_values[p]) == type(1):
                        p_k_v_b = p_k_v_b + "`%s`=%d ," % (p, before_values[p])
                    if type(before_values[p]) == type(u'a'):
                        vl = before_values[p]
                        p_k_v_b = p_k_v_b + "`%s`='%s'," % (p, vl)
                p_k_v_b = p_k_v_b[:-1]
                keys_a = after_values.keys()
                p_k_v_a = ''
                for p in keys_a:
                    if type(after_values[p]) == type(1):
                        p_k_v_a = p_k_v_a + "`%s`=%d and " % (p, after_values[p])
                    if type(after_values[p]) == type(u'a'):
                        # print after_values[p].encode('utf-8')
                        vl = after_values[p]
                        p_k_v_a = p_k_v_a + "`%s`='%s'and " % (p, vl)
                p_k_v_a = p_k_v_a[:-4]
                p = {'before': p_k_v_b, 'after': p_k_v_a}
                sql = "update %s set %s where %s" % (table, p['after'], p['before'])
                result.append(sql)
        return result

    def run_all_analysis(self):
        self.des = ['#########################################']
        if self.log_level == 'all' or self.log_level == 'info':
            self.des.append(u"\n######开始事务,事务pos:%d######" % self.log_pos)
        if self.event_type == 30:
            res_dml = self.insert_format(self.table, self.row)
            res_undo = self.delete_format(self.table, self.row)
            if self.log_level == 'all':
                self.des.append(u"#####发现写入操作#####")
                self.des.append(u'###dml_sql###')
                for i in res_dml:
                    self.des.append(i+';')
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            elif self.log_level == 'info':
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            else:
                for i in res_undo:
                    self.des.append(i+';')

        if self.event_type == 31:
            res_dml = self.update_format(self.table, self.row, ty='dml')
            res_undo = self.update_format(self.table, self.row, ty='undo')
            if self.log_level == 'all':
                self.des.append(u"#####发现更新操作#####")
                self.des.append(u'###dml_sql###')
                for i in res_dml:
                    self.des.append(i+';')
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            elif self.log_level == 'info':
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            else:
                for i in res_undo:
                    self.des.append(i+';')

        if self.event_type == 32:
            res_undo = self.insert_format(self.table, self.row)
            res_dml = self.delete_format(self.table, self.row)
            if self.log_level == 'all':
                self.des.append(u"#####发现删除操作#####")
                self.des.append(u'###dml_sql###')
                for i in res_dml:
                    self.des.append(i+';')
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            elif self.log_level == 'info':
                self.des.append(u'###undo_sql###')
                for i in res_undo:
                    self.des.append(i+';')
            else:
                for i in res_undo:
                    self.des.append(i+';')
        return self.des