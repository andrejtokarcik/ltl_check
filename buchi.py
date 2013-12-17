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

class GeneralizedBuchiAutomaton(NondeterministicFiniteStateAutomaton):
    def __init__(self, *args, **kwargs):
        super(GeneralizedBuchiAutomaton, self).__init__(*args, **kwargs)

    def ungeneralize(self):
        from itertools import product

        new_states = set(product(self.states, range(len(self.final_states) + 1)))
        def new_trans_function(new_state, symbol):
            out = self.trans_function(new_state[0], symbol)
            new_out = set()
            for q in out:
                print len(self.final_states), new_state[1]
                if new_state[1] == len(self.final_states):
                    j = 0
                elif out in self.final_states[new_state[1]]:
                    print new_state == ('p', 0)
                    j = new_state[1] + 1
                else:
                    j = new_state[1]
                new_out.add((q, j))
            return new_out
        new_final_states = set(product(self.states, [len(self.final_states)]))

        return BuchiAutomaton(alphabet=self.alphabet,
                              states=new_states,
                              init_state=(self.init_state, 0),
                              trans_function=new_trans_function,
                              final_states=new_final_states)
