import sys
from collections import defaultdict
from textx import metamodel_from_file, TextXSyntaxError

class BuiltIn:
    def __init__(self,f):
        self.f = f

    def call(self, env, argsev=None):
        return self.f(env, argsev)

def Play(x):
    def f(env, argsev=None):
        global depth
        dmp[depth].append(x)
        depth += 1
    return f

def repeat(env, argsev=[]):
    def f(_, __):
        ml = argsev[0]
        tms = argsev[1]

        for _ in range(tms):
            ml.call(env)
    return BuiltIn(f)

def wait(env, argsev=[]):
    def f(_, __):
        global depth
        tms = argsev[0]

        for _ in range(tms):
            dmp[depth].append(("wait",))
            depth+=1

    return BuiltIn(f)

def wArgs(x):
    def w(env, argsev=[]):
        def f(_, __):
            global depth
            dmp[depth].append((x,)+tuple(argsev))
            depth+=1

        return BuiltIn(f)
    return w

def Overlay(env, argsev=[]):
    def f(_, __):
        global depth
        pd = depth

        mxdpth = depth
        for arg in argsev:
            arg.call(env)
            mxdpth = max(mxdpth, depth)

            depth = pd

        depth = mxdpth

    return BuiltIn(f)


class Env:
    def __init__(self, sup=None):
        self.sup = sup
        self.vals = {}

    def get(self, ID):
        if ID in self.vals:
            return self.vals[ID]
        if self.sup:
            return self.sup.get(ID)
        return None

    def set(self, ID, val):
        if ID in self.vals:
            self.vals[ID] = val
        elif self.supContains(ID):
            self.chainSet(ID, val)
        else:
            self.vals[ID] = val

    def chainSet(self, ID, val):
        if ID in self.vals:
            self.vals[ID] = val
            return
        if self.sup != None:
            self.sup.chainSet(ID, val)

    def supContains(self, ID):
        return self.sup != None and self.sup.get(ID) != None

class Melody:

    def __init__(self, parent, name, args, statements):
        self.parent = parent
        self.name = name
        self.args = args
        self.statements = statements

    def call(self, env, argsev=None):
        def fn(_, __):
            nenv = Env(env)
            for i in range(len(self.args)):
                nenv.set(self.args[i], argsev[i])
            executeBlock(nenv, self.statements)

        if not self.args:
            fn(env, argsev)
        return BuiltIn(fn)

def parse(inp):
    return MM.model_from_str(inp)

def executeProgram(env, prog):
    for m in prog.melodies:
        evaluate(env, m)
    v = prog.melodies[0].call(env)

def executeBlock(env, block):
    env = Env(env)
    for stmt in block:
        evaluate(env, stmt)

def evaluate(env, x):
    envmp = {
            'AssignStmt' : executeAssignStmt,
            'Atom' : evalAtom,
            'Expr' : evalExpr,
            'FuncExpr' : evalFuncExpr,
            'ForStmt' : executeForStmt,
            'IfStmt' : executeIfStmt,
            'KeyStmt' : evalKeyStmt,
            'KID' : evalID,
            'Melody' : evalMelody,
            'Product' : evalProduct,
            'Program' : executeProgram,
    }
    if isinstance(x, int) or isinstance(x, str):
        return x
    if isinstance(x, tuple):
        return x
    return envmp[x.__class__.__name__](env, x)

def evalMelody(env, melody):
    env.set(melody.name, melody)

def evalID(env, ID):
    return env.get(ID)

def evalKeyStmt(env, stmt):
    expr = evaluate(env, stmt.exp)
    if stmt.op == "play":
        expr.call(env)
    else:
        wait(env, [expr]).call(env)

def executeAssignStmt(env, stmt):
    v = evaluate(env, stmt.rhs)
    env.set(stmt.lhs, v)

def executeForStmt(env, stmt):
    env = Env(env)
    a = evaluate(env, stmt.a)
    b = evaluate(env, stmt.b)
    if not (isinstance(a, int) and isinstance(b, int)):
        return
    v = a
    env.set(stmt.it, v)
    for _ in range(a, b+1):
        executeBlock(env, stmt.statements)

        v+=1
        env.set(stmt.it,v)

def executeIfStmt(env, stmt):
    v = evaluate(env, stmt.cond)
    if v:
        executeBlock(env, stmt.then)
    else:
        if len(stmt.elsestmts):
            executeBlock(env, stmt.elsestmts)

def evalFuncExpr(env, func):
    f = evaluate(env, func.op)
    args = list(map(lambda x: evaluate(env, x), func.args))
    if isinstance(f, int) or isinstance(f, str):
        return f
    return f.call(gloE, args)

def evalExpr(env, expr):
    ops = expr.op
    trms = list(map(lambda x: evaluate(env, x), expr.trm))
    sm = trms[0] if len(trms) else 0
    for a, b in zip(ops, trms[1:]):
        if a == '+':
            sm += b
        else:
            sm -= b
    return sm

def evalProduct(env, expr):
    ops = expr.op
    trms = list(map(lambda x: evaluate(env, x), expr.trm))
    prd = trms[0] if len(trms) else 0
    for a, b in zip(ops, trms[1:]):
        if a == '*':
            prd *= b
        else:
            prd //= b
    return prd

def evalAtom(env, at):
    if isinstance(at.trm, int):
        return at.trm
    if isinstance(at.trm, str):
        return env.get(at.trm)
    if isinstance(at.trm, tuple):
        return at.trm[1]
    return evaluate(env, at.trm);

def procDmp(dmp):
    l = len(dmp)
    w = max(map(len,dmp.values()))
    lss = [[("wait",)]*l for _ in range(w)]
    for time in range(l):
        for i in range(len(dmp[time])):
            lss[i][time] = dmp[time][i]
    return lss

def parseToAudio(inp):
    global depth, dmp
    depth = 0
    dmp = defaultdict(list)
    p = parse(inp)
    if p:
        evaluate(gloE, p)
        val = procDmp(dmp)
        return val
    return None


builtins = {
        "Kick" : BuiltIn(Play(("kick",))),
        "Snare" : BuiltIn(Play(("snare",))),
        "Clap" : BuiltIn(Play(("clap",))),
        "HiHat" : BuiltIn(Play(("hihat",))),
        "Piano" : BuiltIn(wArgs("piano")),
        "Sine" : BuiltIn(wArgs("sine")),
        "Square" : BuiltIn(wArgs("square")),
        "Triangle" : BuiltIn(wArgs("triangle")),
        "Sawtooth" : BuiltIn(wArgs("sawtooth")),
        "overlay" : BuiltIn(Overlay),
        "repeat" : BuiltIn(repeat),
        "wait" : BuiltIn(wait),
}

MMFILE = "Calliope/Model.tx"

MM = metamodel_from_file(MMFILE, classes=[Melody])
MM.register_obj_processors({'NoteLit': lambda x: ("NOTE",x)})
gloE = Env()
for a, b in builtins.items():
    gloE.set(a,b)

if __name__ == "__main__":
    depth = 0

    dmp = defaultdict(list)

    lns = sys.stdin.read()
    p = parse(lns)
    if p != None:
        evaluate(gloE, parse(lns))
    print(procDmp(dmp))
