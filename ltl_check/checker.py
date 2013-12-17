from .buchi import buchi_composition
from .kripke import KripkeStructure
from .ltl_formulae import *
from .ltl_graph import LTLGraph

kripke_example = KripkeStructure(init_state='P',
    succs_function=lambda x: {'P': ['V'], 'V': ['V']}[x],
    label_function=lambda x: {'P': [Atom('K')], 'V': [Atom('Z')]}[x])

kripke_example_large = KripkeStructure(init_state='Platba',
    succs_function=lambda x: {'Platba': ['Volba'],
        'Volba': ['Limo', 'Pivo'], 'Limo': ['Platba'],
        'Pivo': ['Platba']}[x],
    label_function=lambda x: {'Platba': [], 'Volba': [Atom('Z')],
        'Limo': [Atom('Z'), Atom('K'), Atom('L')],
        'Pivo': [Atom('Z'), Atom('K'), Atom('P')]}[x])

ltl_example = X(Atom('Z'))

def check(kripke, ltl):
    # I know, I should probably rely much more on duck typing
    # yet these asserts are such nice guards to have when testing.
    assert isinstance(kripke, KripkeStructure)
    assert isinstance(ltl, LTLFormula)

    ba_sys = kripke.to_buchi()
    ltl_neg = negate(ltl)
    ltl_graph = LTLGraph(ltl_neg)
    ltl_graph.expand()
    ba_ltl = ltl_graph.to_generalized_buchi().ungeneralize()
    ba_sync = buchi_composition(ba_sys, ba_ltl)
    print unicode(ba_sync)

    accepting_cycle = ba_sync.nested_dfs()
    if accepting_cycle:
        print "No, the property %s does not hold, a counter-example " \
              "was found:\n%s" % (ltl, accepting_cycle)
    else:
        print "Yes, the property %s does hold." % ltl
