import sys
from textx import metamodel_from_file, TextXSyntaxError

class Env:
    sup = None
    vals = {}
    def __init__(self, sup=None):
        self.sup = sup

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
        nenv = Env(env)
        for i in range(len(self.args)):
            nenv.set(self.args[i], argsev[i])

        executeBlock(nenv, self.statements)

MMFILE = "Model.tx"

MM = metamodel_from_file(MMFILE, classes=[Melody])

gloE = Env()

def parse(inp):
    try:
        model = MM.model_from_str(inp)
    except TextXSyntaxError as err:
        print(err)
        return None
    return model

def executeProgram(env, prog):
    for m in prog.melodies:
        evaluate(env, m)
    prog.melodies[0].call(env)

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
    return envmp[x.__class__.__name__](env, x)

def evalMelody(env, melody):
    env.set(melody.name, melody)

def evalID(env, ID):
    return env.get(ID)

def evalKeyStmt(env, stmt):
    expr = evaluate(env, stmt.exp)
    if stmt.op == "play":
        print(expr)

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
    return evaluate(env, at.trm);

if __name__ == "__main__":
    lns = sys.stdin.read()
    evaluate(gloE, parse(lns))
    print(gloE.vals)
