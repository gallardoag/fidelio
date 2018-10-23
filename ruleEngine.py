#Definiciones sobre Reglas

#   Statement
#       |_childStatements -> StatementCollections
#       |_eval -> Bool

#   Statement_Construction:
#       |_with: aStatementCollection and: anOperatorsCollection
#       |_childStatements <- StatementCollection
#       |_operators <- OperatorsCollection
#       |_eval -> Bool

#   Statement_Leaf:
#       |_with: aRule
#       |_childStatements -> self
#       |_evalRule -> Bool
#       |_eval -> Bool

#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

class Statement():

    def statements(self, parameter_list):
        raise NotImplementedError

    def eval(self, parameter_list):
        raise NotImplementedError

class Statement_Construction():
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
        n = statements.length()
        i = 1
        while ((i < n) and result == True):
            if operators[i] == 'OR':
                result = result or statements[i].eval(parameter_list)
            else:
                result = result and statements[i].eval(parameter_list)

class Statement_Leaf():

    def withRule(self, aRule):
        self._rule = aRule

    def statements(self):
        return [self]

    def evalRule(self, parameter_list):
        return True

    def eval(self, parameter_list):
        return self.evalRule(parameter_list)