import unittest

from test.test_user_login import TestUserLogin
from test.test_user_registration import TestUserRegistration

# Launch all tests from test classes
if __name__ == '__main__':
    test_classes_to_run = [TestUserRegistration, TestUserLogin]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
