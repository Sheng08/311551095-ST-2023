import unittest
from calculator import Calculator


class ApplicationTest(unittest.TestCase):
    params_list1 = [(2, 5), (84, 7), (33, 12), (93, 3), (14, 25)]
    params_list2 = [4, 25, 121, 225, 49]

    def test_add(self):
        '''Test case function for addition'''
        self.calc = Calculator()

        # Test 5 sets of valid input
        expected_list1 = [7, 91, 45, 96, 39]
        for idx, (p1, p2) in enumerate(self.params_list1):
            with self.subTest():
                result = self.calc.add(p1, p2)
                self.assertEqual(result, expected_list1[idx])
        # Test 1 set of invalid input
        with self.assertRaises(TypeError):
            self.calc.add('a', 1)

    def test_divide(self):
        '''Test case function for division'''
        self.calc = Calculator()

        # Test 5 sets of valid input
        expected_list2 = [0.4, 12, 2.75, 31, 0.56]
        for idx, (p1, p2) in enumerate(self.params_list1):
            with self.subTest():
                result = self.calc.divide(p1, p2)
                self.assertEqual(result, expected_list2[idx])
        # Test 1 set of invalid input
        with self.assertRaises(TypeError):
            self.calc.divide(1, 'a')

    def test_sqrt(self):
        '''Test case function for square root'''
        self.calc = Calculator()

        # Test 5 sets of valid input
        expected_list3 = [2, 5, 11, 15, 7]
        for idx, p1 in enumerate(self.params_list2):
            with self.subTest():
                result = self.calc.sqrt(p1)
                self.assertEqual(result, expected_list3[idx])
        # Test 1 set of invalid input
        with self.assertRaises(TypeError):
            self.calc.sqrt('a')

    def test_exp(self):
        '''Test case function for exponentiation'''
        self.calc = Calculator()

        # Test 5 sets of valid input
        expected_list4 = [
            54.598150033144236, 7.200489933738588e+10, 3.5451311827611664e+52,
            5.2030551378848545e+97, 1.9073465724950998e+21
        ]
        for idx, p1 in enumerate(self.params_list2):
            with self.subTest():
                result = self.calc.exp(p1)
                self.assertEqual(result, expected_list4[idx])
        # Test 1 set of invalid input
        with self.assertRaises(TypeError):
            self.calc.exp('a')


if __name__ == '__main__':
    unittest.main()
