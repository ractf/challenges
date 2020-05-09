import sys

from emojasm.execute import OP, has_arg
from emojasm.state import State
from emojasm.execute import execute_instruction

# variation selector 16
comb = chr(0xfe0f) 

def parse_emoji(src, state):
    maxidx = len(src) - 1 # largest valid idx
    c = src[state.PC]
    if state.PC < maxidx and src[state.PC + 1] == comb:
        state.PC += 1
        return c+comb
    return c


def run(src, initial_data=(None, None, None), max_instructions=1000, allow_input=False, outfile=sys.stdout, show_dbg=False):
    state = State(tape_data=initial_data, allow_input=allow_input, outfile=outfile, show_dbg=show_dbg)
    maxidx = len(src) - 1
    dbg_out = "\n\n--Debug output\n\n"
    while True:
        if state.PC > maxidx or state.PC < 0:
            if state.show_dbg:
                dbg_out += f"Halting (pc: {state.PC}, maxidx: {maxidx})\n"
                print(dbg_out, file=state.outfile)
            break
        c = parse_emoji(src, state)
        pre_pc = state.PC

        state.PC += 1 # pointing at the next chr to look at

        try:
            op = OP(c)
        except ValueError:
            continue # if we don't know what it is, skip it

        if op in has_arg:
            # assuming for now all args are one character
            arg = parse_emoji(src, state)
            state.PC += 1 # move it on again
        elif op == OP.LDA:
            # currently the only one with 2 args
            # i don't really like this tbh
            # todo: make better
            arg1 = parse_emoji(src, state)
            state.PC += 1
            arg2 = parse_emoji(src, state)
            state.PC += 1
            arg = [arg1, arg2]
        elif op == OP.LDJMP:
            # and this one has 4
            # fun, isn't it
            arg1 = parse_emoji(src, state)
            state.PC += 1
            arg2 = parse_emoji(src, state)
            state.PC += 1
            arg3 = parse_emoji(src, state)
            state.PC += 1
            arg4 = parse_emoji(src, state)
            state.PC += 1
            arg = [arg1, arg2, arg3, arg4]
        else:
            arg = None

        if state.show_dbg:
            dbg_out += f"{pre_pc}-{state.PC}: {op} with args: {arg}\n"
        #input()
        extra_dbg = execute_instruction(op, state, arg)  # Instructions can provide extra dbg by returning a string
        if state.show_dbg and extra_dbg:
            dbg_out += f"[{op}] - {extra_dbg}\n"
        max_instructions -= 1
        if max_instructions <= 0:
            if state.show_dbg:
                print(dbg_out, file=state.outfile)
            break
