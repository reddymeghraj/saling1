# Copyright (c) 2013, wayzon and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('Sales')

class TestSales(unittest.TestCase):
	pass
