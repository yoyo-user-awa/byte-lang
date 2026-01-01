from re import split as rsplit
from time import sleep as delay

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.console_flush = bytearray()
    def exe(self,code:str):
        lines = code.strip().splitlines()
        lines = [ln for ln in lines if ln.strip()]
        lines = [rsplit(r'\s*,\s*',ln) for ln in lines]
        idx = 0
        while idx < len(lines):
            ln = lines[idx]
            idx += 1
            if not ln:
                continue
            if ''.join(ln).startswith('~!'):
                continue
            w = int(ln[0],16)
            match w:
                case 0: continue
                case 1: Interpreter.__output_ch(int(ln[1],16))
                case 2: Interpreter.__endln()
                case 3:
                    name = str(int(ln[1],16))
                    self.__setvar(name=name, val=int(ln[2],16))
                case 4: Interpreter.__output_ch(self.__getvar(str(int(ln[1], 16))))
                case 5:
                    cur_var = int(ln[1], 16)
                    loop_head = idx
                case 6:
                    if self.__getvar(str(cur_var)) != 0:
                        self.__setvar(str(cur_var), self.__getvar(str(cur_var)) - 1)
                        idx = loop_head
                case 7:
                    delay(int(ln[1],16)/1000000)
                case 0x3a:
                    name = str(int(ln[1], 16))
                    self.__setvar(name=name, val=self.__getvar(name)+1)
                case 0x1a:
                    name = str(int(ln[1], 16))
                    self.__setvar(name=name, val=(ord(input()[0])))
                case 0x5a:
                    name = str(int(ln[1], 16))
                    name1 = str(int(ln[2], 16))
                    if self.__getvar(name) != self.__getvar(name1):
                        idx += int(ln[3], 16)
                case 0x1b:
                    byte = int(ln[1], 16)
                    self.console_flush.append(byte)

                case 0x1ba:
                    print(self.console_flush.decode('utf-8',errors='ignore'), end='')
                case 0x1bb:
                    self.console_flush.clear()

    @staticmethod
    def __output_ch(ch:int) -> None: print(chr(ch),end='')
    @staticmethod
    def __endln() -> None: print()
    def __setvar(self,name:str,val:int) -> None: self.vars.update({name:val})
    def __getvar(self,name:str) -> int: return self.vars.get(name,-616)