class NormalLTLFormula(object):
    pass

class Atom(NormalLTLFormula):
    def __init__(self, id_):
        self.id_ = id_

    def __repr__(self):
        return "Atom(%r)" % self.id_

class Not(NormalLTLFormula):
    def __init__(self, atom):
        assert isinstance(atom, Atom)
        self.atom = atom

    def __repr__(self):
        return "Not(%r)" % self.atom

class Or(NormalLTLFormula):
    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "Or(%r, %r)" % (self.subformula1, self.subformula2)

class And(NormalLTLFormula):
    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "And(%r, %r)" % (self.subformula1, self.subformula2)

class X(NormalLTLFormula):
    def __init__(self, subformula):
        assert isinstance(subformula, NormalLTLFormula)
        self.subformula = subformula

    def __repr__(self):
        return "X(%r)" % self.subformula

class U(NormalLTLFormula):
    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "U(%r, %r)" % (self.subformula1, self.subformula2)

class R(NormalLTLFormula):
    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "R(%r, %r)" % (self.subformula1, self.subformula2)

