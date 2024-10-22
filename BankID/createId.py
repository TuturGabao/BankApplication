"""
This is the part to create a unique ID per username.
It will first create a block (0123) based on the username,
then a second block based on the creation time,
and a third block based on both of these things.

This ID will be necessary to change password if you 
forget your password.   XXXX-XXXX
"""

import binaryConverter
import shifts

SHIFTS = "SLCHLCHCHH"

def _to_ascii(string: str) -> list[str]:
    return [str(ord(char)) for char in string]

def _add_recurrence(ascii_list: list[str]) -> list[str]:
    r_list = []
    for i,th in enumerate(ascii_list):
        recurrence = 0
        for i in range(i,len(ascii_list)):
            th2 = ascii_list[i]
            if th2 == th:
                recurrence+=1
        if recurrence>=10:
            recurrence%=10
        if len(th)==2:
            r_list.append(str(recurrence)+th)
        else:
            r_list.append(th)
    return r_list

def _add_sum(ascii_list: list[str]) -> list[str]:
    r_list = []
    for th in ascii_list:
        sum = 0
        for char in th:
            sum+=int(char)
        if sum>9:
            sum = sum%10
        r_list.append(th+str(sum))
    return r_list

def _whole_shift(ascii_list: list[str]) -> list[str]:
    r_list = []
    for i,th in enumerate(ascii_list):
        shift = SHIFTS[i%10]
        if shift == "S":
            r_list.append(shifts.s_shift(th))
        elif shift == "L":
            r_list.append(shifts.l_shift(th))
        elif shift == "C":
            r_list.append(shifts.c_shift(th))
        elif shift == "H":
            r_list.append(shifts.h_shift(th))
    return r_list

def _rely_number(list: list[list[str]]) -> list[str]:
    r_list = []
    for th in list:
        r_string = ""
        for ch in th:
            if len(ch)>=2:
                ch = str(int(ch)%10)
            r_string+=ch
        r_list.append(r_string)
    return r_list

def create_id(name: str) -> str:
    ascii_name = _to_ascii(name)
    ascii_name = _add_recurrence(ascii_name)
    ascii_name = shifts.left_shift(ascii_name)
    ascii_name = _add_sum(ascii_name)
    ascii_name = _whole_shift(ascii_name)

    binary_name = []
    for th in ascii_name:
        binary_name.append(binaryConverter.text_to_binary(th,4))
    temp = []
    for th in binary_name:
        temp.append(shifts.reverse_shift(th))
    binary_name = temp.copy()
    print(binary_name)

    temp = []
    for th in binary_name:
        temp.append(binaryConverter.binaries_to_text(th))
    binary_name = temp.copy()

    binary_name = _rely_number(binary_name)

    return ascii_name, binary_name

name = "abca"

print(create_id(name)[0])
print("")
print(create_id(name)[1])