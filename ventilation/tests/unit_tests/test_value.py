from unittest import TestCase

from value import Value


class TestValue(TestCase):

    def test_inherited_class_fail_equal_test(self):

        class Child1(Value):
            @property
            def value(self):
                return 1

        class Child2(Value):
            @property
            def value(self):
                return 1

        child1 = Child1()
        child2 = Child2()

        self.assertNotEqual(child1, child2)

    def test_same_class_pass_equal_test(self):

        class Child1(Value):

            @property
            def value(self):
                return 1

        child1 = Child1()
        child2 = Child1()

        self.assertEqual(child1,  child2)

    def test_same_class_pass_less_than_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertTrue(Child(10) < Child(20))

    def test_same_class_fail_less_than_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertFalse(Child(10) < Child(10))

    def test_same_class_pass_less_than_equal_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertTrue(Child(10) <= Child(10))

    def test_same_class_pass_greater_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertTrue(Child(10) > Child(5))

    def test_same_class_fail_greater_equal_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertFalse(Child(10) > Child(10))

    def test_same_class_pass_greater_equal_test(self):

        class Child(Value):

            def __init__(self, value):
                super().__init__()
                self._value = value

        self.assertTrue(Child(10) >= Child(10))


