from .buchi import BuchiAutomaton
from .utils import powerset

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
                self.states.add(state)
                succs_stack += succs_function(state)

        # Obtain the set of atomic propositions.
        self.atoms = set()
        for state in self.states:
            self.atoms.update(label_function(state))

    def to_buchi(self):
        alphabet = powerset(self.atoms)
        def trans_function(state, symbol):
            if set(self.label_function(state)) == set(symbol):
                return self.succs_function(state)

        return BuchiAutomaton(states=self.states,
                              alphabet=alphabet,
                              init_state=self.init_state,
                              trans_function=trans_function,
                              final_states=self.states)
