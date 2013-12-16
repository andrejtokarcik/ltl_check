import time
from ltl_formulae import *   # :(

INIT_EDGE = -1

def negate(formula):
    if isinstance(formula, Atom):
        return Not(formula)
    if isinstance(formula, Not):
        return formula.atom
    return not formula       # XXX: Or check for bool explicitly?


class LTLGraphNode(object):
    id_counter = 0

    def __init__(self, incoming, current=None, in_queue=None, next_=None):
        if current is None:
            current = set()
        if in_queue is None:
            in_queue = set()
        if next_ is None:
            next_ = set()

        self.__class__.id_counter += 1
        self.id_ = self.__class__.id_counter
        self.incoming = set(incoming)
        self.labels = {
            'current': set(current),
            'in_queue': set(in_queue),
            'next': set(next_)
        }

    def __repr__(self):
        return "<LTLGraphNode with ID=%r, incoming=%r, labels=%r>" % \
            (self.id_, self.incoming, self.labels)

class LTLGraph(object):
    def __init__(self, formula):
        assert isinstance(formula, NormalLTLFormula)
        self.start_node = LTLGraphNode(incoming=[INIT_EDGE],
                                       in_queue=[formula])
        self.nodes = set()

    def expand(self, node=None):
        if node is None:
            node = self.start_node

        if not node.labels['in_queue']:
            try:
                n2s = (n2 for n2 in self.nodes
                       if n2.labels['current'] == node.labels['current'] and
                          n2.labels['next'] == node.labels['next'])
                node2 = n2s.next()
                node2.incoming |= node.incoming
            except StopIteration:
                new_node = LTLGraphNode(incoming=[node.id_],
                                        in_queue=node.labels['next'])
                self.nodes.add(node)
                self.expand(new_node)
        else:
            formula = node.labels['in_queue'].pop()
            if formula in node.labels['current']:
                self.expand(node)

            method = getattr(self, '_process_' + formula.__class__.__name__)
            method(node, formula)

    def _process_atomic(self, node, formula):
        if negate(formula) not in node.labels['current']:
            new_current = node.labels['current'] | {formula}
            new_node = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=node.labels['in_queue'],
                                 next_=node.labels['next'])
            self.expand(new_node)

    def _process_Atom(self, *args, **kwargs):
        return self._process_atomic(*args, **kwargs)

    def _process_Not(self, *args, **kwargs):
        return self._process_atomic(*args, **kwargs)

    def _process_Or(self, *args, **kwargs):
        new_current = node.labels['current'] | {formula}

        new_queue1 = node.labels['in_queue'] | {formula.subformula1}
        new_node1 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue1,
                                 next_=node.labels['next'])

        new_queue2 = node.labels['in_queue'] | {formula.subformula2}
        new_node2 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue2,
                                 next_=node.labels['next'])

        self.expand(new_node1)
        self.expand(new_node2)

    def _process_And(self, node, formula):
        new_current = node.labels['current'] | {formula}
        new_queue = node.labels['in_queue'] | {formula.subformula1,
                                               formula.subformula2}
        new_node = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue,
                                 next_=node.labels['next'])

        self.expand(new_node)

    def _process_X(self, node, formula):
        new_current = node.labels['current'] | {formula}
        new_next = node.labels['next'] | {formula.subformula}
        new_node = LTLGraphNode(incoming=node.incoming,
                                current=new_current,
                                in_queue=node.labels['in_queue'],
                                next_=new_next)
        self.expand(new_node)

    def _process_U(self, node, formula):
        new_current = node.labels['current'] | {formula}

        new_queue1 = node.labels['in_queue'] | {formula.subformula1}
        new_next1 = node.labels['next'] | {formula}
        new_node1 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue1,
                                 next_=new_next1)

        new_queue2 = node.labels['in_queue'] | {formula.subformula2}
        new_node2 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue2,
                                 next_=node.labels['next'])

        self.expand(new_node1)
        self.expand(new_node2)

    def _process_R(self, node, formula):
        new_current = node.labels['current'] | {formula}

        new_queue1 = node.labels['in_queue'] | {formula.subformula1,
                                                formula.subformula2}
        new_node1 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue1,
                                 next_=node.labels['next'])

        new_queue2 = node.labels['in_queue'] | {formula.subformula2}
        new_next2 = node.labels['next'] | {formula}
        new_node2 = LTLGraphNode(incoming=node.incoming,
                                 current=new_current,
                                 in_queue=new_queue2,
                                 next_=new_next2)

        self.expand(new_node1)
        self.expand(new_node2)

    def __unicode__(self):
        desc = "Nodes:\n"
        for node in sorted(self.nodes, key=lambda x: x.id_):
            desc += "`-- %s\n" % node
        return desc

