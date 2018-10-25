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

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

class Statement():

    def statements(self, parameter_list):
        raise NotImplementedError

    def eval(self, parameter_list):
        raise NotImplementedError

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

    def statements(self):
        return [self]

    def eval(self, transaction):
        field = self._field
        range = self._range

        if range.start <= range.end:
            return range.start <= transaction.__getattribute__(field) <= range.end
        else:
            return range.start <= transaction.__getattribute__(field) or transaction.__getattribute__(field) <= range.end


class RuleCondition():
    pass
class Range():
    pass
class Transaction():
    pass