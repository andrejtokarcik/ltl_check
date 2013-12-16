class NormalLTLFormula(object):
    @property
    def subformulae(self):
        subs = {self}
        try:
            for i in range(1, self.operands_num + 1):
                sub = getattr(self, 'subformula%d' % i)
                subs.add(sub)
                subs |= sub.subformulae
        except AttributeError:
            pass
        return subs

    @property
    def atoms(self):
        if isinstance(self, Atom):
            return {self}
        if isinstance(self, Not):
            return {self.atom}

        res = set()
        for subformula in self.subformulae:
            if subformula == self:
                continue
            res.update(subformula.atoms)
        return res

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
    operands_num = 2

    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "Or(%r, %r)" % (self.subformula1, self.subformula2)

class And(NormalLTLFormula):
    operands_num = 2

    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "And(%r, %r)" % (self.subformula1, self.subformula2)

class X(NormalLTLFormula):
    operands_num = 1

    def __init__(self, subformula1):
        assert isinstance(subformula1, NormalLTLFormula)
        self.subformula1 = subformula1

    def __repr__(self):
        return "X(%r)" % self.subformula1

class U(NormalLTLFormula):
    operands_num = 2

    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "U(%r, %r)" % (self.subformula1, self.subformula2)

class R(NormalLTLFormula):
    operands_num = 2
    def __init__(self, subformula1, subformula2):
        assert isinstance(subformula1, NormalLTLFormula)
        assert isinstance(subformula2, NormalLTLFormula)
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def __repr__(self):
        return "R(%r, %r)" % (self.subformula1, self.subformula2)

def negate(iter_or_formula):
    try:
        result = set()
        for i in iter_or_formula:
            result.add(negate(i))
        return result
    except TypeError:
        if isinstance(iter_or_formula, Atom):
            return Not(iter_or_formula)
        if isinstance(iter_or_formula, Not):
            return iter_or_formula.atom
        return not iter_or_formula       # XXX: Or check for bool explicitly?
