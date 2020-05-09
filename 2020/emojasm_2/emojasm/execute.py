from enum import Enum
from emojasm.state import CmpFlag

class OP(Enum):
    # opcode definitions go here
    TF = "➡️"
    TB = "⬅️"
    TRW = "⏪"
    
    TIN = "👁️"
    TOUT = "✏️"

    ADD = "➕"
    AND = "🍴"
    OR = "🎷"
    INC = "💡"
    DEC = "🦔"

    OUT = "📤"
    IN = "📥"

    TAR = "📦"
    TRA = "🎁"
    TXY = "🔨"
    TYX = "⛏️"
    XYX = "⚒️"

    CMP = "❓"
    CMPZ = "❔"

    JMP = "🐰"
    JMPEQ = "⚖️"
    JMPNEQ = "🏷️"

    LDA = "✉️"
    LDJMP = "🐇"

    HLT = "🗿"

    PS = "🐝"

has_arg = [
    OP.TF, OP.TB, OP.TIN, OP.TOUT,
    OP.INC, OP.DEC, OP.ADD, OP.AND, OP.OR,
    OP.TAR, OP.TRA, OP.TRW,
    OP.CMP, OP.CMPZ
]

tape_emoji = {
    "📼": 0,
    "🎞️": 1,
    "🎥": 2
}

reg_emoji = {
    "🔨" : "X",
    "⛏️" : "Y",
    "🗃️" : "A"
}

literal_emoji = [
    "😀", # 0
    "😁", # 1
    "😂", # 2
    "😃", # 3
    "😄", # 4
    "😅", # 5
    "😆", # 6
    "😇", # 7
    "😈", # 8
    "😉", # 9
    "😊", # A
    "😋", # B
    "😌", # C
    "😍", # D
    "😎", # E
    "😏"  # F
]

def execute_instruction(op, state, arg):
    #print(op, state, arg)
    fn = globals()["inst_"+op.name.lower()]
    return fn(state, arg)
    #print(op, arg, state)

def gettape(state, arg):
    if arg not in tape_emoji:
        raise ValueError("Invalid tapeid: {}".format(arg))
    tapeid = tape_emoji[arg]
    return state.T[tapeid]

def getreg(arg):
    if arg not in reg_emoji:
        raise ValueError("Invalid register id: {}".format(arg))
    return reg_emoji[arg]

# instruction functions
def inst_tf(state, arg):
    gettape(state, arg).fd()
def inst_tb(state, arg):
    gettape(state, arg).bk()
def inst_trw(state, arg):
    gettape(state, arg).rw()


def inst_tin(state, arg):
    state.R.A = gettape(state, arg).I
def inst_tout(state, arg):
    gettape(state, arg).set_write(state.R.A)


def inst_add(state, arg):
    state.R.A = state.R.A + getattr(state.R, getreg(arg))
def inst_and(state, arg):
    state.R.A = state.R.A & getattr(state.R, getreg(arg))
def inst_or(state, arg):
    state.R.A = state.R.A | getattr(state.R, getreg(arg))
def inst_inc(state, arg):
    setattr(state.R, getreg(arg), getattr(state.R, getreg(arg))+1)
def inst_dec(state, arg):
    setattr(state.R, getreg(arg), getattr(state.R, getreg(arg))-1)


def inst_out(state, arg):
    print(chr(state.R.A), end='', file=state.outfile)
    if state.show_dbg:
        return f"Outputting {chr(state.R.A)}"
def inst_in(state, arg):
    if state.allow_input:
        from emojasm.getch import getch
        state.R.A = ord(getch())
    else:
        state.R.A = 0

def inst_tar(state, arg):
    setattr(state.R, getreg(arg), state.R.A)
def inst_tra(state, arg):
    state.R.A = getattr(state.R, getreg(arg))
def inst_txy(state, arg):
    state.R.Y = state.R.X
def inst_tyx(state, arg):
    state.R.X = state.R.Y
def inst_xyx(state, arg):
    tmp = state.R.X
    state.R.X = state.R.Y
    state.R.Y = tmp

def cmpflags(a, b):
    f = CmpFlag.NONE
    if a == b:
        f |= CmpFlag.EQ
    return f

def inst_cmp(state, arg):
    state.CF = cmpflags(getattr(state.R, getreg(arg)), state.R.A)
def inst_cmpz(state, arg):
    state.CF = cmpflags(getattr(state.R, getreg(arg)), 0)

def inst_jmp(state, arg):
    state.PC = state.R.JMP
    if state.show_dbg:
        return f"Setting PC to {state.R.JMP}"
def inst_jmpeq(state, arg):
    if state.CF & CmpFlag.EQ:
        return inst_jmp(state, arg)
def inst_jmpneq(state, arg):
    if not state.CF & CmpFlag.EQ:
        return inst_jmp(state, arg)

def inst_lda(state, args):
    msb = args[0]
    lsb = args[1]
    val = (literal_emoji.index(msb)<<4)|literal_emoji.index(lsb)
    state.R.A = val

def inst_ldjmp(state, args):
    hi = args[0]
    himid = args[1]
    lomid = args[2]
    lo = args[3]
    val = (literal_emoji.index(hi)<<12)|(literal_emoji.index(himid)<<8)|(literal_emoji.index(lomid)<<4)|literal_emoji.index(lo)
    state.R.JMP = val
    if state.show_dbg:
        return f"Setting RJMP to {val} for ldjmp [0x{literal_emoji.index(hi):01x}, 0x{literal_emoji.index(himid):01x}, 0x{literal_emoji.index(lomid):01x}, 0x{literal_emoji.index(lo):01x}]"

def inst_hlt(state, arg):
    state.PC = -1 # tells run to stop execution

def inst_ps(state, arg):
    print(state, file=state.outfile)
