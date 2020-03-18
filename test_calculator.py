import unittest
import calculator


class TestCalc(unittest.TestCase):
    """ AB """

    def test_add(self):
        """ AB """
        res = calculator.add(4, 3)
        self.assertEqual(res, 7)
        self.assertEqual(calculator.add(-1, 1), 0)
        self.assertEqual(calculator.add(-1, -1), -2)
        # print("Add")

    def test_division(self):
        """ AB """
        self.assertEqual(calculator.division(8, 2), 4)
        self.assertRaises(ZeroDivisionError, calculator.division, 10, 0)
        with self.assertRaises(ZeroDivisionError):
            calculator.division(20, 0)
        # print("Divide")


if __name__ == "__main__":
    unittest.main()
