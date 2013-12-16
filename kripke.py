from itertools import chain, combinations
from buchi import BuchiAutomaton

def powerset(iterable):
    s = list(iterable)
    return set(chain.from_iterable(combinations(s, r)
                                   for r in range(len(s)+1)))

class KripkeStructure(object):
    def __init__(self, init_state, succs_function, label_function):
        self.init_state = init_state
        self.succs_function = succs_function
        self.label_function = label_function

        # Generate states using the succs function (pretty naively).
        self.states = set()
        succs_stack = [init_state]
        while succs_stack:
            state = succs_stack.pop()
            if state not in self.states:
                succs_stack += succs_function(state)
                self.states.add(state)

        # Obtain the set of atomic propositions.
        self.atoms = set()
        for state in self.states:
            self.atoms.update(label_function(state))

    def as_buchi(self):
        alphabet = powerset(self.atoms)
        def trans_function(state, symbol):
            assert state in self.states
            assert symbol in alphabet
            if set(self.label_function(state)) == set(symbol):
                return self.succs_function(state)

        return BuchiAutomaton(states=self.states,
                              alphabet=alphabet,
                              init_state=self.init_state,
                              trans_function=trans_function,
                              final_states=self.states)
