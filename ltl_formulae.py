class NormalLTLFormula(object):
    pass

class Atom(NormalLTLFormula):
    def __init__(self, identifier):
        self.identifier = identifier

class Not(NormalLTLFormula):
    def __init__(self, atom):
        assert isinstance(atom, AtomicProposition)
        self.atom = atom

class Or(NormalLTLFormula):
    def __init__(self, formula1, formula2):
        assert isinstance(formula1, NormalLTLFormula)
        assert isinstance(formula2, NormalLTLFormula)
        self.formula1 = formula1
        self.formula2 = formula2

class And(NormalLTLFormula):
    def __init__(self, formula1, formula2):
        assert isinstance(formula1, NormalLTLFormula)
        assert isinstance(formula2, NormalLTLFormula)
        self.formula1 = formula1
        self.formula2 = formula2

class X(NormalLTLFormula):
    def __init__(self, formula):
        assert isinstance(formula, NormalLTLFormula)
        self.formula = formula

class U(NormalLTLFormula):
    def __init__(self, formula1, formula2):
        assert isinstance(formula1, NormalLTLFormula)
        assert isinstance(formula2, NormalLTLFormula)
        self.formula1 = formula1
        self.formula2 = formula2

class R(NormalLTLFormula):
    def __init__(self, formula1, formula2):
        assert isinstance(formula1, NormalLTLFormula)
        assert isinstance(formula2, NormalLTLFormula)
        self.formula1 = formula1
        self.formula2 = formula2
