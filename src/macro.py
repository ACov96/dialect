from context import Context
from copy import deepcopy

class Macro:
    def __init__(self):
        self.macros = []

    def register_macro(self, macro_def, macro_statements):
        self.macros.append((macro_def, macro_statements))

    def has_macro(self, statement):
        for macro_def, _ in self.macros:
            if self._match_macro(macro_def, statement):
                return True
        return False

    def _match_macro(self, macro_def, statement):
        if len(macro_def) != len(statement):
            return False
        for macro_el, statement_el in zip(macro_def, statement):
            if macro_el[0] == 'atom' or statement_el == 'atom':
                if not (macro_el[0] == 'atom' and statement_el[0] == 'atom' and macro_el[1] == statement_el[1]):
                    return False
        return True

    def render_statements(self, statement):
        ctx = Context()
        if self.has_macro(statement):
            macro_args, macro_statements = self._find_macro(statement)
        else:
            print('BAD MACRO')
            return []
        for arg, stmt in zip(macro_args, statement):
            if arg[0] == 'placeholder':
                ctx.set(arg, stmt)
        def _render_statement(stmt):
            if isinstance(stmt, tuple) or isinstance(stmt, list):
                for i in range(len(stmt)):
                    convert = False
                    if isinstance(stmt[i], tuple):
                        stmt[i] = list(stmt[i])
                        convert = True
                    if isinstance(stmt[i], list) and stmt[i][0] == 'placeholder':
                        stmt[i] = ctx.get(stmt[i][1])
                    elif isinstance(stmt[i], list):
                        stmt[i] = _render_statement(stmt[i])
                    if convert:
                        stmt[i] = tuple(stmt[i])
            return stmt
        return _render_statement(macro_statements)
        

    def _find_macro(self, statement):
        for macro_def, stmts in self.macros:
            if self._match_macro(macro_def, statement):
                return deepcopy(macro_def), deepcopy(stmts)
