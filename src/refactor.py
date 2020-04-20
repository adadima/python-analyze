from ast import *


class CallFinder(NodeVisitor):
    """
    Abstract Syntax Tree Visitor for finding
    the locations of all the function calls in
    an AST.

    Calling `visit()` on the root of an AST would
    return a list of tuples of the form
    (line_start_i, col_start_i, line_end_i, col_end_i)
    containing the line and column bounds of the i-th
    function call in the code.
    """
    def generic_visit(self, node):

        call_locations = []
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        call_locations += self.visit(item)
            elif isinstance(value, AST):
                call_locations += self.visit(value)
        return call_locations

    def visit_Call(self, node):
        func = node.func
        child_values = self.generic_visit(node)
        call_location = (func.lineno, func.col_offset, func.end_lineno, func.end_col_offset)
        if isinstance(func, Attribute):
            return child_values
        return [call_location] + child_values


def convert(replacer, path_to_input, path_to_output):
    """
    Given a replacement string, an input Python source file and an
    output file location, writes the contents of the
    input file to the output file, but with all the
    function calls changed to calls to replacer.
    """
    ast_ = get_ast(path_to_input)
    call_locations = CallFinder().visit(ast_)
    lineno_to_calls = {}
    for call_loc in sorted(call_locations):
        lineno_to_calls.setdefault(call_loc[0], []).append(call_loc)

    new_lines = replace_calls(replacer,
                              lineno_to_calls,
                              sorted(lineno_to_calls.keys()),
                              readLines(path_to_input))
    writeLines(new_lines, path_to_output)


def get_ast(path_to_source):
    """
    Retireve the abstract syntax tree of the code
    found in the `path_to_source` file
    :param path_to_source: location of the source file
    :return: an AST object, the root of the abstract syntax
    tree describing the code in the given file
    """
    with open(path_to_source, 'r') as source_file:
        source_code = "".join(source_file.readlines())

    return parse(source_code)


def readLines(path_to_source):
    """
    Opens the filename at the given path,
    reads the contents and returns a list
    of all the lines.
    """
    with open(path_to_source, 'r') as code:
        return code.readlines()


def writeLines(lines, path_to_output):
    """
    Writes a list of strings ( one per line )
    in a file found at `path_to_output`.
    :param lines: list of strings, the lines to be written
    :param path_to_output: path to the file to be written
    """
    with open(path_to_output, 'w') as new_source:
        new_source.writelines(lines)


def replace_calls(replacer, locations, start_locations, source_lines):
    """
    Replaces the lines of a source file such that all the function calls
    in that file are converted to repalcer()
    :param replacer: the string to replace all function calls with
    :param locations: a dictionary mapping line indices to a list of all
                     the function call locations on the corresponding line

                     ex: {1: (1, 7, 1, 14)} means that there's a function call
                     on line 1 between column offsets 7 and 14.
    :param start_locations: Sorted list of all distinct lines where a function call
                            starts
    :param source_lines: a list containing all lines in the source file ( as strings )
    :return: a list containing all lines in the modified source file ( as strings )
    """
    new_lines = []
    next_call_idx = 0
    next_line_with_call = start_locations[0]
    line_idx = 1

    while line_idx <= len(source_lines):
        if line_idx != next_line_with_call:
            new_lines.append(source_lines[line_idx - 1])
            line_idx += 1
        else:
            new_line, line_idx = span_call(line_idx - 1,
                                        locations[next_line_with_call],
                                        source_lines,
                                        replacer)
            new_lines.append(new_line)
            try:
                next_call_idx += 1
                next_line_with_call = start_locations[next_call_idx]
            except IndexError:
                print("You've replaced all function calls already!")
    return new_lines


def span_call(line_idx, call_locations, source_lines, replacer):
    """
    Takes in a line index and returns a string representing a new line
    in which all the function calls that initially started on `line_idx`
    are replaced with the value of `replacer`

    :param line_idx: the index of the line to modify
    :param call_locations: a list of tuples, represents the line/column bounds
                           of all function calls that start on `line_idx`
    :param source_lines:  a list of all the lines in the source code
    :param replacer: the string to repalce all function calls with
    :return: A string representing the line with all the function calls
            starting at line `line_idx` converted to calls to `replacer`
    """
    current_line = source_lines[line_idx]
    new_line = []
    remaining = current_line

    for i, loc in enumerate(call_locations):
        line1, col1, line2, col2 = loc
        if line1 != line2:
            new_line.append(replacer)
            new_line.append(source_lines[line2][col2:])
            break
        separator = current_line[col1:col2]
        to_keep, fn, remaining = remaining.partition(separator)
        new_line.append(to_keep)
        if remaining:
            new_line.append(replacer)
    else:
        new_line.append(remaining)
    return "".join(new_line), call_locations[-1][2] + 1


if __name__=='__main__':
    convert('foo', '../data/12749338.txt', './new_code.txt')
