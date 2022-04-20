#!/usr/bin/env python3
import sys
from typing import Dict

class BooleanModel:
    def __init__(self):
        self.term_freq = {}
        self.text_with_term = {}
        self.skipped = set()
        self.freq_bound = float('inf')

    def remove_term(self, term):
        self.term_freq.pop(term)
        self.text_with_term.pop(term)

    def process_text(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            line = f.readline()
            while len(line): # return empty str if EOF
                terms = line.split()
                for term in terms:
                    if self.term_freq.get(term, 0) + 1 > self.freq_bound: # get rid of high freq term
                        self.skipped.add(term)
                        self.remove_term(term)
                    if term in self.skipped: continue
                    self.term_freq[term] = self.term_freq.get(term, 0) + 1
                    self.text_with_term[term] = self.text_with_term.get(term, set()) | set([path])
                line = f.readline()

    def get_set(self, term):
        return self.text_with_term.get(term)

    def operation(self, set1, set2, operation):
        if operation == 'OR':
            return set1 | set2
        return set1 & set2 # case: operation == 'AND'

    def query(self, operations):
        operations = list(operations)
        stack = []
        for ch in operations:
            if ch == ')':
                set1 = stack.pop()
                operator = stack.pop()
                set2 = stack.pop()
                stack.pop() # '('
                if isinstance(set1,str):
                    set1 = self.get_set(set1)
                if isinstance(set2,str):
                    set2 = self.get_set(set2)
                ch = self.operation(set1, set2, operator)
            stack.append(ch)
        return stack[0] or -1 # -1 if not found
