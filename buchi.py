from itertools import product

class NondeterministicFiniteStateAutomaton(object):
    def __init__(self, states, alphabet, init_state, trans_function,
                 final_states):
        assert init_state in states

        self.states = states
        self.alphabet = alphabet
        self.init_state = init_state
        # TODO: Ensure that the transition function always returns a state
        # (i.e., a member of the states set).
        self.trans_function = trans_function
        self.final_states = final_states

    def to_graph(self):
        edges = set()
        for state in self.states:
            for symbol in self.alphabet:
                for succ in self.trans_function(state, symbol):
                    edges.add((state, succ))
        return edges

    def nested_dfs(self):
        visited = set()
        nested = set()
        stack = set()

        def dfs(vertex):
            if vertex not in visited:
                visited.add(vertex)
                stack.add(vertex)
                for (v, s) in self.to_graph():
                    if v == vertex:
                        result = dfs(s)
                        if result:
                            return result
                if self.is_accepting(vertex):
                    result = detect_cycle(vertex)
                    if result:
                        return result
                stack.remove(vertex)

        def detect_cycle(vertex):
            if vertex not in nested:
                nested.add(vertex)
                for (v, s) in self.to_graph():
                    if v == vertex:
                        if s in stack:
                            return stack
                        else:
                            result = detect_cycle(s)
                            if result:
                                return result

        return dfs(self.init_state)

    def __unicode__(self):
        states_list = list(self.states)
        states_out = map(unicode, states_list)
        states_out[states_list.index(self.init_state)] += " (initial)"
        # FIXME: hidden assumption
        #for final_state in self.final_states:
        #    states_out[states_list.index(final_state)] += " (final)"

        desc = "States: %s\n" % ", ".join(states_out)
        desc += "Final states: %s\n" % self.final_states
        desc += "Alphabet: %s\n" % ", ".join(map(unicode, list(self.alphabet)))
        desc += "\n"
        desc += "Transition function:\n"
        for state in self.states:
            for symbol in self.alphabet:
                new_state = self.trans_function(state, symbol)
                if new_state:
                    desc += "  (%s, %s) -> %s\n" % (state, symbol, new_state)
        return desc

class BuchiAutomaton(NondeterministicFiniteStateAutomaton):
    def __init__(self, *args, **kwargs):
        super(BuchiAutomaton, self).__init__(*args, **kwargs)

    def is_accepting(self, state):
        return state in self.final_states

class GeneralizedBuchiAutomaton(NondeterministicFiniteStateAutomaton):
    def __init__(self, *args, **kwargs):
        super(GeneralizedBuchiAutomaton, self).__init__(*args, **kwargs)

    def ungeneralize(self):
        new_states = set(product(self.states, range(len(self.final_states) + 1)))
        def new_trans_function((p, i), symbol):
            out = self.trans_function(p, symbol)
            new_out = set()
            for q in out:
                if i == len(self.final_states):
                    j = 0
                elif out in self.final_states[new_state[1]]:
                    j = i + 1
                else:
                    j = i
                new_out.add((q, j))
            return new_out
        new_final_states = set(product(self.states, [len(self.final_states)]))

        return BuchiAutomaton(alphabet=self.alphabet,
                              states=new_states,
                              init_state=(self.init_state, 0),
                              trans_function=new_trans_function,
                              final_states=new_final_states)

def buchi_composition(ba1, ba2):
    assert ba1.alphabet == ba2.alphabet
    assert ba1.final_states == ba1.states

    new_states = set(product(ba1.states, ba2.states))
    def new_trans_function((ba1_state, ba2_state), symbol):
        ba1_out = ba1.trans_function(ba1_state, symbol)
        ba2_out = ba2.trans_function(ba2_state, symbol)
        return set(product(ba1_out, ba2_out))
    new_final_states = product(ba1.states, ba2.final_states)

    return BuchiAutomaton(state=new_states,
                          alphabet=ba1.alphabet,
                          init_state=(ba1.init_state, ba2.init_state),
                          trans_function=new_trans_function,
                          final_states=new_final_states)
