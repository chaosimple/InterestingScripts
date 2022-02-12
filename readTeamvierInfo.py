#!/usr/bin/env python
#coding:utf-8
"""
  Author : Chao Wang -- (chaosimpler@gmail.com)
  License: LGPL clause
  Created: 2022/2/12
  Purpose: 获取Teamviewer的运行数据
    
"""

import win32gui,win32con,win32api
import array        
import time

TV_PATH = r"D:\Program Files (x86)\TeamViewer\TeamViewer.exe"
WAIT_TIME = 5


#----------------------------------------------------------------------
def get_Hwnd():
    """
    打开TeamViewer 窗口，返回ID和Password的Handle
    AddTime:	
        2022/2/12 by ChaoWang
    """
    hn1 = win32gui.FindWindow(None, 'TeamViewer')
    while hn1 == 0:
        # 如果程序没有运行，则打开该程序
        win32api.ShellExecute(0, 'open', TV_PATH, "", "", 0)
        time.sleep(WAIT_TIME)        
        hn1 = win32gui.FindWindow(None, 'TeamViewer')
        
        
    hn2 = win32gui.FindWindowEx(hn1, None, 'MainWindowRemoteControlPage', None)
    hn3 = win32gui.FindWindowEx(hn2, None, 'IncomingRemoteControlComponentView',None)
    
    # 该子窗口中包含两个相同的 CustomRunner 组件
    hn4 = win32gui.FindWindowEx(hn3, None, 'CustomRunner', None)
    id_hwnd = win32gui.FindWindowEx(hn4, None, 'Edit', None)
    hn5 = win32gui.FindWindowEx(hn3, hn4, 'CustomRunner', None)
    pwd_hwnd = win32gui.FindWindowEx(hn5, None, 'Edit', None)

    return id_hwnd, pwd_hwnd

#----------------------------------------------------------------------
def get_Text(hwnd):
    """返回指定 Handle对应的Edit中的文字
        
    AddTime:	
        2022/2/12 by ChaoWang
    """
    buffer_len = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1
    buffer = array.array('b', b'\x00\x00' * buffer_len)
    text_len = win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buffer_len, buffer)
    text = win32gui.PyGetString(buffer.buffer_info()[0], buffer_len - 1)
    return text
    

#----------------------------------------------------------------------
def getTV_Info():
    """
    获取TeamViewer的账号和密码信息
    
    使用 Spy++ 读取特定程序中子窗口及各个控件类的信息，
    然后 使用 win32 api 读取文本框中的内容
    
    注意：
    # FindWindowEx() 只能查找直接子窗口，因此需要逐级查找
    # 该函数的第二个参数用于表示在哪个子窗口继续查找，用于查找包含两个相同类名的子窗口
    
    参考：
    https://github.com/wuxc/pywin32doc/blob/master/md/win32gui.md#win32guifindwindowex
    """
    
    # 获取指定 Handle
    id_hwnd, pwd_hwnd = get_Hwnd()

    ID = get_Text(id_hwnd)
    # 如果数据还未生成，则重新读取
    while len(ID) < 6:
        # 保证Teamviewer 本身是正常运行
        id_hwnd, pwd_hwnd = get_Hwnd()
        ID = get_Text(id_hwnd)
    Password = get_Text(pwd_hwnd)
    print("ID:",ID, "Password:",Password)          
    return ID, Password
    
    
if __name__ == '__main__':
    ID, PWD = getTV_Info()
    print('over')