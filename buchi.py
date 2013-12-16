class NondeterministicFiniteStateAutomaton(object):
    def __init__(self, states, alphabet, init_state, trans_function,
                 final_states):
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
        for final_state in self.final_states:
            states_out[states_list.index(final_state)] += " (final)"

        desc = "States: %s\n" % ", ".join(states_out)
        desc += "Alphabet: %s\n" % ", ".join(map(unicode, list(self.alphabet)))
        desc += "\n"
        desc += "Transition function:\n"
        for state in self.states:
            for symbol in self.alphabet:
                new_state = self.trans_function(state, symbol)
                if new_state is not None:
                    desc += "  (%s, %s) -> %s\n" % (state, symbol, new_state)
        return desc

class BuchiAutomaton(NondeterministicFiniteStateAutomaton):
    def __init__(self, *args, **kwargs):
        super(BuchiAutomaton, self).__init__(*args, **kwargs)

class GeneralizedBuchiAutomaton(NondeterministicFiniteStateAutomaton):
    def __init__(self, *args, **kwargs):
        super(GeneralizedBuchiAutomaton, self).__init__(*args, **kwargs)
