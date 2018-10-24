from ruleEngine import *
import datetime

def aDateWithinRangeEvaluatesTrue():
    transaction = {}
    purchase = {}
    purchase['purchaseDate'] = datetime.datetime(2018, 9, 16, 0, 0)
    transaction['purchase'] = purchase
    
    fromDate = datetime.datetime(2012, 9, 16, 0, 0)
    toDate = datetime.datetime(2019, 9, 16, 0, 0)

    ruleCondition = {}
    range = {}
    range['start'] = fromDate
    range['end'] = toDate
    item = 'purchase'
    field = 'purchaseDate'
    ruleCondition['range'] = range
    ruleCondition['item'] = item
    ruleCondition['field'] = field

    rule = RangeRule(ruleCondition)
    assert rule.eval(transaction) == True 

aDateWithinRangeEvaluatesTrue()
    
