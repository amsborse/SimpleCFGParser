#refered and modified from : https://gist.github.com/bufas/65022d522b5bb31cc0d9 
class State(object):
    def __init__(self, currentLabel, rules, dot, i, j, id, producer):
        self.currentLabel = currentLabel
        self.rules = rules
        self.dot = dot
        self.i = i
        self.j = j
        self.id = id
        self.producer = producer

    def next(self):
        """Returns the tag after the dot"""
        return self.rules[self.dot]

    def complete(self):
        return len(self.rules) == self.dot

    def __eq__(self, other):
        return (self.currentLabel == other.currentLabel and
                self.rules == other.rules and
                self.dot == other.dot and
                self.i == other.i and
                self.j == other.j)

    def __str__(self):
        rule_string = ''
        for i, rule in enumerate(self.rules):
            if i == self.dot:
                rule_string += '•'
            rule_string += rule + ' '
        if self.dot == len(self.rules):
            rule_string += '•'
        return 'S%d %s -> %s \t\t\t [%d, %d]  %s' % (self.id, self.currentLabel, rule_string, self.i, 
                                                self.j, self.producer)

class Parser:
    def __init__(self, words, grammar, terminals):
        self.chart = [[] for _ in range(len(words) + 1)]
        self.current_id = 0
        self.words = words
        self.grammar = grammar
        self.terminals = terminals

    def get_new_id(self):
        self.current_id += 1
        return self.current_id - 1

    def is_terminal(self, tag):
        return tag in self.terminals

    def is_complete(self, state):
        return len(state.rules) == state.dot

    def enqueue(self, state, chart_entry):
        if state not in self.chart[chart_entry]:
            self.chart[chart_entry].append(state)
        else:
            self.current_id -= 1

    def predictor(self, state):
        for production in self.grammar[state.next()]:
            self.enqueue(State(state.next(), production, 0, state.j, state.j, self.get_new_id(), 'predictor'), state.j)

    def scanner(self, state):
        if self.words[state.j] in self.grammar[state.next()]:
            self.enqueue(State(state.next(), [self.words[state.j]], 1, state.j, state.j + 1, self.get_new_id(), 'scanner'), state.j + 1)

    def completer(self, state):
        for s in self.chart[state.i]:
            if not s.complete() and s.next() == state.currentLabel and s.j == state.i and s.currentLabel != 'λ':
                self.enqueue(State(s.currentLabel, s.rules, s.dot + 1, s.i, state.j, self.get_new_id(), 'completer'), state.j)

    def parse(self):
        self.enqueue(State('λ', ['S'], 0, 0, 0, self.get_new_id(), 'dummy start state'), 0)
        for i in range(len(self.words) + 1):
            for state in self.chart[i]:
                if not state.complete() and not self.is_terminal(state.next()):
                    self.predictor(state)
                elif i != len(self.words) and not state.complete() and self.is_terminal(state.next()):
                    self.scanner(state)
                else:
                    self.completer(state)

    def __str__(self):
        res = ''
        
        for i, chart in enumerate(self.chart):
            res += '\nChart[%d]\n' % i
            if len(chart) == 0:
                print("Chart creation incomplete")
                exit()
            for state in chart:
                res += str(state) + '\n'

        return res
 
