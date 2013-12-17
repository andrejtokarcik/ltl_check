from itertools import product

class NondeterministicFiniteStateAutomaton(object):
    def __init__(self, states, alphabet, init_state, trans_function,
                 final_states):
        assert init_state in states

        self.states = states
        self.alphabet = set(alphabet) #frozenset(map(frozenset, alphabet))
        self.init_state = init_state
        self.trans_function = self._wrapper(trans_function)
        self.final_states = final_states

    def _wrapper(self, tf):
        def trans_function(state, symbol):
            assert state in self.states
            #assert symbol in self.alphabet
            res = set(tf(state, symbol) or [])
            if res:
                assert res.issubset(self.states)
            return res
        return trans_function

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
        final_states = list(self.final_states)

        def new_trans_function((p, i), symbol):
            out = self.trans_function(p, symbol)
            new_out = set()
            for q in out:
                if i == len(final_states):
                    j = 0
                elif q in final_states[i]:
                    j = i + 1
                else:
                    j = i
                new_out.add((q, j))
            return new_out
        new_final_states = set(product(self.states, [len(final_states)]))

        return BuchiAutomaton(alphabet=self.alphabet,
                              states=new_states,
                              init_state=(self.init_state, 0),
                              trans_function=new_trans_function,
                              final_states=new_final_states)

def buchi_composition(ba_sys, ba_ltl):
    assert ba_sys.alphabet.issuperset(ba_ltl.alphabet)
    assert ba_sys.final_states == ba_sys.states

    new_states = set(product(ba_sys.states, ba_ltl.states))
    def new_trans_function((ba_sys_state, ba_ltl_state), symbol):
        ba_sys_out = ba_sys.trans_function(ba_sys_state, symbol)
        ba_ltl_out = ba_ltl.trans_function(ba_ltl_state, symbol)
        return set(product(ba_sys_out or [], ba_ltl_out or []))
    new_final_states = set(product(ba_sys.states, ba_ltl.final_states))

    return BuchiAutomaton(states=new_states,
                          alphabet=ba_sys.alphabet,
                          init_state=(ba_sys.init_state, ba_ltl.init_state),
                          trans_function=new_trans_function,
                          final_states=new_final_states)
