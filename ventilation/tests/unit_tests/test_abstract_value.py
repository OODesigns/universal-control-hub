from unittest import TestCase

from abstract_value import AbstractValue


class TestAbstractValue(TestCase):

    def test_inherited_class_fail_equal_test(self):

        class Child1(AbstractValue):
            @property
            def value(self):
                return 1

        class Child2(AbstractValue):
            @property
            def value(self):
                return 1

        child1 = Child1()
        child2 = Child2()

        self.assertNotEqual(child1, child2)

    def test_same_class_pass_equal_test(self):

        class Child1(AbstractValue):

            @property
            def value(self):
                return 1

        child1 = Child1()
        child2 = Child1()

        self.assertEqual(child1, child2)

