import enum, sys

TAPELENGTH = 256

class Tape:
    def __init__(self, tapeid, length=TAPELENGTH, initial_data=None):
        self.id = tapeid
        if initial_data is None:
            self.data = bytearray(length)
        else:
            self.data = bytearray.fromhex(initial_data)
        self.pos = 0 # tape position
        self.I = 0 # input reg
        self._O = 0 # output reg
        self._W = False # write-on-next-move
    
    def __repr__(self):
        return "<Tape({0.id}), {0.pos} @ [{1}]>".format(self, self.data.hex())
    
    def fd(self):
        # 0. silently fail if pos == 256 already
        # 1. set I to current byte
        # 2. if write set, set current byte to O (and write to false)
        # 3. increment pos.
        if self.pos >= len(self.data):
            return
        self.I = self.data[self.pos]
        if self._W:
            self.data[self.pos] = self._O
            self._W = False
        self.pos += 1
    
    def bk(self):
        # if pos == 0, silently fail
        # decrement pos (no read or write when going backwards)
        if self.pos == 0:
            return
        self.pos -= 1
    
    def rw(self):
        # 1. rewind tape to 0
        # 2. set I and O to 0
        # 3. clear W flag
        self.pos = 0
        self.I = 0
        self._O = 0
        self._W = False
    
    def set_write(self, value):
        # set W flag to True
        # set O to value
        self._W = True
        self._O = value

class RegisterContainer:
    def __init__(self):
        self._X = 0
        self._Y = 0
        self._A = 0
    def __repr__(self):
        return "<Reg X={0.X} Y={0.Y} A={0.A}>".format(self)
    
    @property
    def X(self):
        return self._X
    @X.setter
    def X(self, val):
        self._X = val & 0xff

    @property
    def Y(self):
        return self._Y
    @Y.setter
    def Y(self, val):
        self._Y = val & 0xff
		
    @property
    def JMP(self):
        return self._A
    @JMP.setter
    def JMP(self, val):
        self._A = val & 0xffff

    @property
    def A(self):
        return self._A & 0xff
    @A.setter
    def A(self, val):
        self._A = val & 0xff

class CmpFlag(enum.Flag):
    NONE = 0
    EQ = enum.auto()

class State:
    def __init__(self, tape_data=(None, None, None), allow_input=True, outfile=sys.stdout, show_dbg=False):
        self.T = [
            Tape(0, initial_data=tape_data[0]),
            Tape(1, initial_data=tape_data[1]),
            Tape(2, initial_data=tape_data[2])
        ]
        self.R = RegisterContainer()
        self.PC = 0
        self.CF = CmpFlag.NONE
        self.allow_input = allow_input
        self.outfile = outfile
        self.show_dbg = show_dbg
    def __repr__(self):
        return "<State @{0.PC} T={0.T} R={0.R} F={0.CF}>".format(self)
