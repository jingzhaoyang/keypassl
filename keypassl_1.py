#!/usr/bin/env python
#coding=utf-8

import sys,threading
from select import select
import virtkey,time
from kptool.keepassdb import keepassdb

# password = raw_input('请输入密码：',)
password = ""

def put_key(key):
    v = virtkey.virtkey()
    for i in str(key):
        v.press_unicode(ord(i))
        v.release_unicode(ord(i))
class MyWindow( QtGui.QWidget ):
    def __init__( self ):
        super( MyWindow, self ).__init__()
        self.creat_menu()
        self.doExit()            
    def monitor_action(self):
        global hot_key_down
        if hot_key_down == 1 :
            self.creat_menu()
            hot_key_down = 0
    def creat_menu(self):
        self.menu = {}
        level = {
           0:0,
           1:0,
           2:0,
           #level : last_parent_id
           }
        self.user_action={}
        self.pass_action={}
        menuBar = QtGui.QMenuBar()
        self.menu[0] = QtGui.QMenu('1',menuBar)
        old_level = 0
        k = keepassdb.KeepassDBv1(r"/home/jing/文档/x-y-t.kdb", password)
        for g in k.get_groups():
            self.menu[g['group_id']] = QtGui.QMenu(g['title'])
            self.get_userandpass(k,g['group_id'])
            if g['level'] == old_level :
                self.menu[level[g['level']]].addMenu(self.menu[g['group_id']])
                level[g['level']+1] = g['group_id']
                old_level = g['level']
            elif g['level'] > old_level:
                self.menu[level[g['level']]].addMenu(self.menu[g['group_id']])
                old_level = g['level']
            else :
                self.menu[level[g['level']]].addMenu(self.menu[g['group_id']])
                level[g['level']+1] = g['group_id']
                old_level = g['level']
        self.Exit_menu = self.menu[0].addAction("Exit")
        self.Exit_menu.triggered.connect(QtCore.QCoreApplication.instance().quit)
        point = QtCore.QPoint()
        point = QtGui.QCursor.pos()
        self.menu[0].exec_(point)
        self.menu[0].close()


    def get_userandpass(self,k,groupid):
        user_action = {}
        pass_action = {}
        for e in k.get_entries_from_groupid(groupid):
            if e['id'] != '00000000000000000000000000000000':
                self.menu[e['id']] = QtGui.QMenu(e['title'])
                self.menu[e['group_id']].addMenu(self.menu[e['id']])
                self.user_action[e['id']] = self.menu[e['id']].addAction(e['username'])
                self.pass_action[e['id']] = self.menu[e['id']].addAction(e['password'])
                self.user_action[e['id']].triggered.connect(self.do_stuff_caller(e['username']))
                self.pass_action[e['id']].triggered.connect(self.do_stuff_caller(e['password']))



    def doStuff(self, item):
        put_key(item)
    def do_stuff_caller(self,item):
        return lambda: self.doStuff(item)
        
    def doExit(self):
        self.close()
        sys.exit(0)
        
if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    demo = MyWindow()
    demo.show()
    app.exec_()
