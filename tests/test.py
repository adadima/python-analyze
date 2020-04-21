import os
import unittest
from ast import *
from refactor import convert


class SmallIntegrationTest(unittest.TestCase):

    def run_test(self, input_file, expected):
        convert('foo', input_file, "./out.txt")

        with open("./out.txt", 'r') as f:
            result = f.readlines()

        with open(expected, 'r') as f:
            exp = f.readlines()
        os.remove("./out.txt")
        self.assertEqual(exp, result)

    def test_one_per_line(self):
        self.run_test("resources/test1.py", "resources/expected1.txt")

    def test_chained_calls(self):
        self.run_test("resources/test2.py", "resources/expected2.txt")

    def test_multiple_per_line(self):
        self.run_test("resources/test3.py", "resources/expected3.txt")

    def test_multiline_lambda(self):
        self.run_test("resources/test4.py", "resources/expected4.txt")

    def test_multiline_subscript(self):
        self.run_test("resources/test5.py", "resources/expected5.txt")

    def test_class_attributes(self):
        self.run_test("resources/test6.py", "resources/expected6.txt")

    def test_class_constructor(self):
        self.run_test("resources/test7.py", "resources/expected7.txt")


class TestVisitor(NodeVisitor):

    def __init__(self, expected):
        self.expected = expected

    def generic_visit(self, node):
        is_ok = True

        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        is_ok = is_ok and self.visit(item)
            elif isinstance(value, AST):
                is_ok = is_ok and self.visit(value)

        return is_ok

    def visit_Call(self, node):
        is_ok = True
        if not isinstance(node.func, Attribute):
            is_ok = isinstance(node.func, Name) and node.func.id == self.expected
        return is_ok and self.generic_visit(node)


class CodeforcesIntegrationTest(unittest.TestCase):
    test_visitor = TestVisitor('foo')

    def assert_file(self, inp_path, out_path):
        try:
            convert('foo', inp_path, out_path)
            with open(out_path, 'r') as f:

                    code = "".join(f.readlines())
                    ast_ = parse(code)
            os.remove(out_path)
            self.assertTrue(self.test_visitor.visit(ast_),
                        "Some Call nodes may not have been converted to `foo`"
                        f"for file {inp_path}:\n{code}")
        except SyntaxError:
            self.assertTrue(True)

    def test_large(self):
        for _, _, submissions in os.walk('../data/'):
            for file in submissions:
                self.assert_file(f"../data/{file}", "out.txt")


if __name__ == "__main__":
    pass
