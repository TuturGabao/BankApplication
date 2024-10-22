from typing import Union

def s_shift(arg: Union[int, str]) -> int | str:
    if isinstance(arg, int):
        string = str(arg)
        return int("".join([string[1], string[0], string[3], string[2]]))
    else:
        return "".join([arg[1], arg[0], arg[3], arg[2]])
    
def l_shift(arg: Union[int, str]) -> int | str:
    if isinstance(arg, int):
        string = str(arg)
        return int("".join([string[3], string[2], string[1], string[0]]))
    else:
        return "".join([arg[3], arg[2], arg[1], arg[0]])
    
def c_shift(arg: Union[int, str]) -> int | str:
    if isinstance(arg, int):
        string = str(arg)
        return int("".join([string[2], string[3], string[0], string[1]]))
    else:
        return "".join([arg[2], arg[3], arg[0], arg[1]])
    
def h_shift(arg: Union[int, str]) -> int | str:
    if isinstance(arg, int):
        string = str(arg)
        return int("".join([string[0], string[3], string[2], string[1]]))
    else:
        return "".join([arg[0], arg[3], arg[2], arg[1]])
    
def whole_shift(string):
    r_string = ""
    for char in string:
        if char=="0":
            r_string=r_string+"1"
        else: r_string=r_string+"0"
    return r_string

def _change_num(string, pos):
    r_string = ""
    for i,char in enumerate(string):
        if i==pos:
            if string[pos]=="1":
                r_string = r_string+"0"
            else:
                r_string = r_string+"1"
        else:
            r_string = r_string+char
    return r_string

def left_shift(list: list[str]) -> list[str]:
    r_list = []
    for th in list:
        r_string = ""
        for i in range(1, len(th)):
            r_string+=th[i]
        r_string+=th[0]
        r_list.append(r_string)
    return r_list

def reverse_shift(list: list[str]) -> list[str]:
    r_list = []
    for i,th in enumerate(list):
        r_list.append(_change_num(th, i))
    return r_list
    