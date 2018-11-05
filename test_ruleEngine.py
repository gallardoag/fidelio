import datetime
import unittest

from ruleEngine import *

class TestRuleMethods(unittest.TestCase):
    
    def setUp(self):
        self.ruleCondition = RuleCondition()
        self.ruleCondition.operand = 'a in b'
        
        self.dateRange = Range()
        self.dateRange.start = datetime.datetime.now() - datetime.timedelta(days=1)
        self.dateRange.end = datetime.datetime.now() + datetime.timedelta(days=1)

        self.amountRange = Range()
        self.amountRange.start = 50
        self.amountRange.end = 150

        self.transaction = Transaction()
        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 100
        self.transaction.purchaseCode = 200
        self.transaction.clientId = 300

    def test_aFieldNotFoundInTransactionRaisesException(self):
        self.ruleCondition.field = 'inexistentField'
        self.ruleCondition.range = self.dateRange
        rule = RangeRule(self.ruleCondition)

        self.assertRaises(AttributeError, rule.eval, self.transaction)

class TestValueRuleMethods(unittest.TestCase):

    def setUp(self):
        self.ruleCondition = RuleCondition()
        self.transaction = Transaction()
        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 100
        self.transaction.purchaseCode = 200
        self.transaction.clientId = 300

    def test_aGreaterThanComparisonIsTrueWhenFieldIsGreaterThanExpected(self):
        self.ruleCondition.field = 'purchaseAmount'
        self.ruleCondition.operand = 'a > b'
        self.ruleCondition.value = 50
        rule = ValueRule(self.ruleCondition)
        self.assertTrue(rule.eval(self.transaction))

    def test_aLessThanComparisonIsTrueWhenFieldIsLessThanExpected(self):
        self.ruleCondition.field = 'purchaseAmount'
        self.ruleCondition.operand = 'a < b'
        self.ruleCondition.value = 500
        rule = ValueRule(self.ruleCondition)
        self.assertTrue(rule.eval(self.transaction))

class TestRangeRuleMethods(unittest.TestCase):

    def setUp(self):
        self.ruleCondition = RuleCondition()
        self.ruleCondition.operand = 'a in b'
        
        self.dateRange = Range()
        self.dateRange.start = datetime.datetime.now() - datetime.timedelta(days=1)
        self.dateRange.end = datetime.datetime.now() + datetime.timedelta(days=1)

        self.amountRange = Range()
        self.amountRange.start = 50
        self.amountRange.end = 150

        self.transaction = Transaction()
        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 100
        self.transaction.purchaseCode = 200
        self.transaction.clientId = 300
            
    def test_aDateWithinRangeEvaluatesTrue(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        rule = RangeRule(self.ruleCondition)

        self.assertTrue(rule.eval(self.transaction))
    
    def test_aDateOutsideRangeEvaluatesFalse(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        rule = RangeRule(self.ruleCondition)

        self.transaction.purchaseDate = self.dateRange.start - datetime.timedelta(days=1)
        self.assertFalse(rule.eval(self.transaction))

        self.transaction.purchaseDate = self.dateRange.end + datetime.timedelta(days=1)
        self.assertFalse(rule.eval(self.transaction))

class TestCompositionMethods(unittest.TestCase):

    def setUp(self):
        self.ruleCondition = RuleCondition()
        self.ruleCondition.operand = 'a in b'

        self.dateRange = Range()
        self.dateRange.start = datetime.datetime.now() - datetime.timedelta(days=1)
        self.dateRange.end = datetime.datetime.now() + datetime.timedelta(days=1)

        self.amountRange = Range()
        self.amountRange.start = 50
        self.amountRange.end = 150

        self.transaction = Transaction()
        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 100
        self.transaction.purchaseCode = 200
        self.transaction.clientId = 300
    
    def test_anOrCompositionIsTrueWhenAnyStatementIsTrue(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        firstRule = RangeRule(self.ruleCondition)

        secondRuleCondition = RuleCondition()
        secondRuleCondition.field = 'purchaseAmount'
        secondRuleCondition.range = self.amountRange
        secondRuleCondition.operand = 'a in b'
        secondRule = RangeRule(secondRuleCondition)

        orStatementConstruction = StatementConstruction([firstRule, secondRule], ['OR'])
        self.assertTrue(orStatementConstruction.eval(self.transaction))

        self.transaction.purchaseDate = self.dateRange.start - datetime.timedelta(days=1)
        orStatementConstruction = StatementConstruction([firstRule, secondRule], ['OR'])
        self.assertTrue(orStatementConstruction.eval(self.transaction))

        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 200
        orStatementConstruction = StatementConstruction([firstRule, secondRule], ['OR'])
        self.assertTrue(orStatementConstruction.eval(self.transaction))

    def test_anOrCompositionIsFalseWhenAllStatementAreFalse(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        firstRule = RangeRule(self.ruleCondition)

        secondRuleCondition = RuleCondition()
        secondRuleCondition.field = 'purchaseAmount'
        secondRuleCondition.range = self.amountRange
        secondRuleCondition.operand = 'a in b'
        secondRule = RangeRule(secondRuleCondition)

        self.transaction.purchaseDate = self.dateRange.start - datetime.timedelta(days=1)
        self.transaction.purchaseAmount = 200
        orStatementConstruction = StatementConstruction([firstRule, secondRule], ['OR'])
        self.assertFalse(orStatementConstruction.eval(self.transaction))

    def test_anAndCompositionIsTrueWhenAllStatementAreTrue(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        firstRule = RangeRule(self.ruleCondition)

        secondRuleCondition = RuleCondition()
        secondRuleCondition.field = 'purchaseAmount'
        secondRuleCondition.range = self.amountRange
        secondRuleCondition.operand = 'a in b'
        secondRule = RangeRule(secondRuleCondition)

        orStatementConstruction = StatementConstruction([firstRule, secondRule], ['AND'])
        self.assertTrue(orStatementConstruction.eval(self.transaction))

    def test_anAndCompositionIsFalseWhenAnyStatementIsFalse(self):
        self.ruleCondition.field = 'purchaseDate'
        self.ruleCondition.range = self.dateRange
        firstRule = RangeRule(self.ruleCondition)

        secondRuleCondition = RuleCondition()
        secondRuleCondition.field = 'purchaseAmount'
        secondRuleCondition.range = self.amountRange
        secondRuleCondition.operand = 'a in b'
        secondRule = RangeRule(secondRuleCondition)

        self.transaction.purchaseDate = self.dateRange.start - \
            datetime.timedelta(days=1)
        orStatementConstruction = StatementConstruction(
            [firstRule, secondRule], ['AND'])
        self.assertFalse(orStatementConstruction.eval(self.transaction))

        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 200
        orStatementConstruction = StatementConstruction(
            [firstRule, secondRule], ['AND'])
        self.assertFalse(orStatementConstruction.eval(self.transaction))

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.ruleEngine = RuleEngine()

        self.valueRuleCondition = RuleCondition()
        self.valueRuleCondition.field = 'purchaseAmount'
        self.valueRuleCondition.operand = 'a > b'
        self.valueRuleCondition.value = 50

        self.dateRange = Range()
        self.dateRange.start = datetime.datetime.now() - datetime.timedelta(days=1)
        self.dateRange.end = datetime.datetime.now() + datetime.timedelta(days=1)
        
        self.rangeRuleCondition = RuleCondition()
        self.rangeRuleCondition.field = 'purchaseDate'
        self.rangeRuleCondition.operand = 'a in b'
        self.rangeRuleCondition.range = self.dateRange


        self.amountRange = Range()
        self.amountRange.start = 50
        self.amountRange.end = 150

        self.transaction = Transaction()
        self.transaction.purchaseDate = datetime.datetime.now()
        self.transaction.purchaseAmount = 100
        self.transaction.purchaseCode = 200
        self.transaction.clientId = 300
    
    def test_allRulesGetEvaluated(self):
        valueSimpleStatement = ValueRule(self.valueRuleCondition)
        rangeSimpleStatement = RangeRule(self.rangeRuleCondition)
        statementOperator = 'OR'
        statements = [valueSimpleStatement, statementOperator]
        operators = [statementOperator]
        compositeStatement = StatementConstruction(statements, operators)
        self.ruleEngine.addStatement(compositeStatement)
        self.ruleEngine.addStatement(valueSimpleStatement)
        self.ruleEngine.addStatement(rangeSimpleStatement)
        tx = self.transaction
        result = self.ruleEngine.eval(tx)
        for ruleEvaluation in result:
            self.assertTrue(ruleEvaluation)

    def test_givenARuleAndAConsequence_WhenTheRuleApplies_ThenTheConsequenceHappens(self):
        prepareFunctions()
        self.ruleEngine.addStatement(statement, consequence)
        prepareTx()
        self.ruleEngine.evalAndExecute(tx)
        checkFunctionsResults()


if __name__ == '__main__':
    unittest.main()
