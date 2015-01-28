# coding:utf-8

# Gently ripped from:
# http://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python

import ctypes

wcscpy = ctypes.cdll.msvcrt.wcscpy

OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
CF_UNICODETEXT = 13

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GMEM_DDESHARE = 0x2000


def get():
    OpenClipboard(None)
    handle = GetClipboardData(CF_UNICODETEXT)
    data = ctypes.c_wchar_p(handle).value
    pcontents = GlobalLock(handle)
    data = ctypes.c_wchar_p(pcontents).value if pcontents else u''
    GlobalUnlock(handle)
    CloseClipboard()
    return data


def put(data):
    if not isinstance(data, unicode):
        data = data.decode('mbcs')
    OpenClipboard(None)
    EmptyClipboard()
    hCd = GlobalAlloc(GMEM_DDESHARE, 2 * (len(data) + 1))
    pchData = GlobalLock(hCd)
    wcscpy(ctypes.c_wchar_p(pchData), data)
    GlobalUnlock(hCd)
    SetClipboardData(CF_UNICODETEXT, hCd)
    CloseClipboard()