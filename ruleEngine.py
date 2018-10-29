#Definiciones sobre Reglas

#   GenericStatement
#       |_childStatements -> StatementCollections
#       |_eval -> Bool

#   StatementConstruction:
#       |_with: aStatementCollection and: anOperatorsCollection
#       |_childStatements <- StatementCollection
#       |_operators <- OperatorsCollection
#       |_eval -> Bool

#   GenericRule:
#       |_with: aRuleCondition
#       |_childStatements -> self
#       |_eval -> Bool

#   GenericRangeRule:
#       |_with: aRange
#       |_childStatements -> self
#       |_eval -> Bool

#   TimeRangeRule:
#       |_with: aTimeRange
#       |_childStatements -> self
#       |_eval -> Bool

#   CodeRule:
#       |_with: aCode
#       |_childStatements -> self
#       |_eval -> Bool

#   CodeRangeRule:
#       |_with: aCodeRange
#       |_childStatements -> self
#       |_eval -> Bool

# class Statement():

#     def statements(self, parameter_list):
#         raise NotImplementedError

#     def eval(self, parameter_list):
#         raise NotImplementedError
#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

import operator

operators = {
'a + b' : operator.add,
'seq1 + seq2' : operator.concat,
'obj in seq' : operator.contains,
'a / b' : operator.truediv,
'a // b' : operator.floordiv,
'a & b' : operator.and_,
'a ^ b' : operator.xor,
'~ a' : operator.invert,
'a | b' : operator.or_,
'a ** b' : operator.pow,
'a is b' : operator.is_,
'a is not b' : operator.is_not,
'obj[k] = v' : operator.setitem,
'del obj[k]' : operator.delitem,
'obj[k]' : operator.getitem,
'a << b' : operator.lshift,
'a % b' : operator.mod,
'a * b' : operator.mul,
'- a' : operator.neg,
'not a' : operator.not_,
'+ a' : operator.pos,
'a >> b' : operator.rshift,
# 'seq * i' : operator.repeat,
'seq[i:j] = values' : operator.setitem,
'del seq[i:j]' : operator.delitem,
'seq[i:j]' : operator.getitem,
's % obj' : operator.mod,
'a - b' : operator.sub,
'obj' : operator.truth,
'a < b' : operator.lt,
'a <= b' : operator.le,
'a == b' : operator.eq,
'a != b' : operator.ne,
'a >= b' : operator.ge,
'a > b' : operator.gt,
}

class StatementConstruction():
    def __init__(self, aStatementCollection, anOperatorsCollection):
        self._childStatements = aStatementCollection
        self._operators = anOperatorsCollection

    def statements(self):
        return self._childStatements

    def operators(self):
        return self._operators

    def eval(self, parameter_list):
        statements = self.statements()
        operators = self.operators()
        result = statements[0].eval(parameter_list)
        n = len(statements)
        i = 1
        while ((i < n)):
            if operators[i-1] == 'OR':
                result = result or statements[i].eval(parameter_list)
            else:
                result = result and statements[i].eval(parameter_list)
            i += 1
        return result

class RangeRule():

    def __init__(self, aRuleCondition):
        self._range = aRuleCondition.range
        self._field = aRuleCondition.field
        self._operand = aRuleCondition.operand

    def statements(self):
        return [self]

    def eval(self, transaction):
        field = self._field
        range = self._range
        result = range.start <= transaction.__getattribute__(field) <= range.end
        if self._operand == 'a in b':
            return result
        else: 
            return not(result)

class ValueRule():

    def __init__(self, aRuleCondition):
        self._value = aRuleCondition.value
        self._field = aRuleCondition.field
        self._operand = aRuleCondition.operand

    def statements(self):
        return [self]

    def eval(self, transaction):
        field = self._field
        value = self._value
        operand = self._operand
        return operators[operand](transaction.__getattribute__(field), value)

class RuleCondition():
    pass
class Range():
    pass
class Transaction():
    pass

class RuleEngine():
    pass