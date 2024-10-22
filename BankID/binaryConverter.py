from typing import Union

def _add_zeros(string, zeros):
    while len(string) < zeros:
        string = "0"+string
    return string

def to_simple_binary(number: int) -> str:
    return _add_zeros("{0:1b}".format(number), 4) if number <= 255 else "Number too big"
    
def to_binary(number: Union[int, str]) -> str:
    if isinstance(number, int):
        return _add_zeros("{0:1b}".format(number), 8) if number <= 255 else "Number too big"
    elif isinstance(number, str):
        return _add_zeros("{0:1b}".format((ord(number))), 8) if len(number)<2 and len(number)!=0 else "Only convert one character!"    

def text_to_binary(text: str, zeros: int) -> list[str]:
    return [_add_zeros("{0:1b}".format(int(char)), zeros) for char in text]

def binary_to_text(binary: str) -> str:
    return str(int(binary, base=2))

def binaries_to_text(binary: list[str]) -> list[str]:
    return [str(int(th, base=2)) for th in binary] 

print(binaries_to_text(['0111', '1001', '1000', '0010']))
