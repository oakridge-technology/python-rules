from sqlalchemy.orm.attributes import InstrumentedAttribute

from logic_engine.rule_bank.rule_bank import RuleBank
from logic_engine.rule_type.aggregate import Aggregate


class Count(Aggregate):

    _as_count_of = ""
    _child_role_name = ""
    _where = ""

    def __init__(self, derive: InstrumentedAttribute, as_count_of: str, where: str):
        super(Count, self).__init__(derive)
        self._as_count_of = as_count_of  # could probably super-ize parent accessor
        self._from_parent_role = as_count_of
        self._where = where
        rb = RuleBank()
        rb.deposit_rule(self)

    def __str__(self):
        if self._where != "":
            result = super().__str__() + f'Count({self._as_count_of} Where {self._where})'
        else:
            result = super().__str__() + f'Count({self._as_count_of})'
        return result

    def execute(self):
        raise Exception("TODO major")

