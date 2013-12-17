from .buchi import buchi_composition
from .ltl_formulae import negate

def check(kripke, ltl):
    ba_sys = kripke.to_buchi()
    neg_ltl = negate(ltl)
    ba_ltl = neg_ltl.to_generalized_buchi().ungeneralize()
    ba_sync = buchi_composition(ba_sys, ba_ltl)

    accepting_cycle = ba_sync.nested_dfs()
    if accepting_cycle:
        print "No, the property '%s' does not hold, a counter-example " \
              "was found:\n%s" % (ltl, accepting_cycle)
    else:
        print "Yes, the property '%s' does hold." % ltl
