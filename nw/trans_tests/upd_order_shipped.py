"""
PyCharm sets PythonPath to the root folder, VSC does not by default - imports fail
Hence, add this to the launch config:
"env": {"PYTHONPATH": "${workspaceFolder}:${env:PYTHONPATH}"}

ref: https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code
"""

import os
import sys
from datetime import datetime

from sqlalchemy import inspect, MetaData
from sqlalchemy.ext.declarative import declarative_base

cwd = os.getcwd()   # eg, /Users/val/python/pycharm/python-rules/nw/trans_tests
required_path_python_rules = cwd  # seeking /Users/val/python/pycharm/python-rules
required_path_python_rules = required_path_python_rules.replace("/nw/trans_tests", "")

sys_path = ""
required_path_present = False
for each_node in sys.path:
    sys_path += each_node + "\n"
    if each_node == required_path_python_rules:
        required_path_present = True

if not required_path_present:
    print("Fixing path (so can run from terminal)")
    sys.path.append(required_path_python_rules)
else:
    pass
    print("NOT Fixing path (default PyCharm, set in VSC Launch Config)")

path_info = "Run Environment info...\n\n"\
            + "Current Working Directory: " + cwd + "\n\n"\
            + "sys.path: (Python imports)\n" + sys_path + "\n"\
            + "From: " + sys.argv[0] + "\n\n"\
            + "Using Python: " + sys.version + "\n\n"\
            + "At: " + str(datetime.now()) + "\n\n"
print("\n" + path_info + "\n\n")


import nw.nw_logic.models as models
from logic_engine.exec_row_logic.logic_row import LogicRow
from logic_engine.util import row_prt, prt
from nw import nw_logic
from nw.nw_logic import session  # opens db, activates logic listener <--

def toggle_order_shipped():
    """ toggle Shipped Date, to trigger balance adjustment """
    """ also test join.
    session.query(Customer).join(Invoice).filter(Invoice.amount == 8500).all()
    """

    pre_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
    session.expunge(pre_cust)

    print("")
    test_order = session.query(models.Order).filter(models.Order.Id == 11011).join(models.Employee).one()
    if test_order.ShippedDate is None or test_order.ShippedDate == "":
        test_order.ShippedDate = str(datetime.now())
        print(prt("Shipping order - ShippedDate: ['' -> " + test_order.ShippedDate + "]"))
    else:
        test_order.ShippedDate = None
        print(prt("Returning order - ShippedDate: [ -> None]"))
    insp = inspect(test_order)
    session.commit()

    print("")
    post_cust = session.query(models.Customer).filter(models.Customer.Id == "ALFKI").one()
    logic_row = LogicRow(row=pre_cust, old_row=post_cust, ins_upd_dlt="*", nest_level=0, a_session=session, row_cache=None)

    if abs(post_cust.Balance - pre_cust.Balance) == 960:
        logic_row.log("Correct adjusted Customer Result")
        assert True
    else:
        row_prt(post_cust, "\nERROR - incorrect adjusted Customer Result")
        print("\n--> probable cause: Order customer update not written")
        row_prt(pre_cust, "\npre_alfki")
        assert False


toggle_order_shipped()
print("\nupd_order_shipped, ran to completion")

