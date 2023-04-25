import unittest
from unittest.mock import patch, PropertyMock
from course_scheduling_system import *


class CSSTest(unittest.TestCase):

    def setUp(self):
        self.stub_check_course_exist = patch.object(CSS,
                                                    "check_course_exist",
                                                    return_value=True)

    # Let check_course_exist return True by mocking (Stub). Try to add one course by add_course, check its return value, and verify the result by get_course_list.
    def test_q1_1(self):
        with self.stub_check_course_exist as stub_check_course_exist:
            css = CSS()
            result = css.add_course(('Algorithms', 'Monday', 3, 4))
            self.assertEqual(result, True)
            self.assertEqual(css.get_course_list(),
                             [('Algorithms', 'Monday', 3, 4)])

    # Let check_course_exist return True by mocking. Try to add two courses overlapping with each other, check its return value, and verify the result.
    def test_q1_2(self):
        with self.stub_check_course_exist as stub_check_course_exist:
            css = CSS()
            result = css.add_course(('Algorithms', 'Monday', 3, 4))
            self.assertEqual(result, True)
            result = css.add_course(('Data Structures', 'Monday', 3, 4))
            self.assertEqual(result, False)
            self.assertEqual(css.get_course_list(),
                             [('Algorithms', 'Monday', 3, 4)])

    # Let check_course_exist return False by mocking. Try to add one course, and check its return value.
    @patch.object(CSS, "check_course_exist", return_value=False)
    def test_q1_3(self, mock_check_course_exist):
        # with patch.object(CSS, "check_course_exist", return_value=False) as stub_check_course_exist:
        css = CSS()
        result = css.add_course(('Algorithms', 'Monday', 3, 4))
        self.assertEqual(result, False)

    # Let check_course_exist return True by mocking. Try to add a invalid course input, and check the Exception raised.
    def test_q1_4(self):
        with self.stub_check_course_exist as stub_check_course_exist:
            css = CSS()
            with self.assertRaises(TypeError):
                css.add_course(('Algorithms', 'Monday', 3, 4, 5))

    # Let check_course_exist return True by mocking. Try to add three courses that don’t overlapp with each other and then remove the second one by remove_course, verify the result, and then check the call count of check_course_exist. Also, try to print out the schedule in a formatted way.
    def test_q1_5(self):
        with self.stub_check_course_exist as stub_check_course_exist:
            css = CSS()
            result = css.add_course(('Algorithms', 'Monday', 3, 4))
            self.assertEqual(result, True)
            result = css.add_course(('Data Structures', 'Monday', 5, 6))
            self.assertEqual(result, True)
            result = css.add_course(('Machine Learning', 'Tuesday', 1, 2))
            self.assertEqual(result, True)
            result = css.remove_course(('Data Structures', 'Monday', 5, 6))
            self.assertEqual(result, True)
            self.assertEqual(css.get_course_list(),
                             [('Algorithms', 'Monday', 3, 4),
                              ('Machine Learning', 'Tuesday', 1, 2)])
            self.assertEqual(stub_check_course_exist.call_count, 4)
            print(css)

    # Add some more (possibly 0) tests to achieve 100% coverage of course_scheduling_system.py. You can mock check_course_exist and use pragma to excluding check_course_exist from coverage analysis.
    def test_q1_6(self):
        with self.stub_check_course_exist as stub_check_course_exist:
            css = CSS()
            result = css.add_course(('Algorithms', 'Monday', 3, 4))
            self.assertEqual(result, True)
            result = css.add_course(('Data Structures', 'Monday', 5, 6))
            self.assertEqual(result, True)
            result = css.add_course(('Machine Learning', 'Tuesday', 1, 2))
            self.assertEqual(result, True)
            result = css.remove_course(('Data Structures', 'Monday', 5, 6))
            self.assertEqual(result, True)
            self.assertEqual(css.get_course_list(),
                             [('Algorithms', 'Monday', 3, 4),
                              ('Machine Learning', 'Tuesday', 1, 2)])
            self.assertEqual(stub_check_course_exist.call_count, 4)

            with self.assertRaises(TypeError):
                css.add_course(('Algorithms', 'Monday', 3, 4, 5))
            with self.assertRaises(TypeError):
                css.add_course((311551000, 'Monday', 3, 4))
            with self.assertRaises(TypeError):
                css.add_course(('Algorithms', 'May', 3, 4))
            with self.assertRaises(TypeError):
                css.add_course(('Algorithms', 'Monday', '3', '4'))

            result = css.remove_course(('Deep Learning', 'Monday', 3, 4))
            self.assertEqual(result, False)

        with patch.object(CSS, "check_course_exist",
                          return_value=False) as stub_check_course_exist:
            css = CSS()
            result = css.remove_course(('Algorithms', 'Monday', 3, 4))
            self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
