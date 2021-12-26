def no_op(value):
    return value

def line_splitter(sep="", formatter=no_op):
    if "" == sep:
        def line_parser(l):
            return [formatter(c) for c in l]
    else:
        def line_parser(l):
            return [formatter(c) for c in l.split(sep)]
    return line_parser

def parse_line(file_name, line_parser=no_op):
    with open(file_name, "r") as input_file:
        for line in input_file:
            return line

def parse_lines(file_name, line_parser=no_op):
    with open(file_name, "r") as input_file:
        return [line_parser(l.strip()) for l in input_file]

def scan_lines(file_name, line_parser=no_op):
    with open(file_name, "r") as input_file:
        for line in input_file:
            yield line_parser(line.strip())

def scan_line_sections(file_name, line_parsers=[no_op]):
    parser_index = 0
    with open(file_name, "r") as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                yield line_parsers[parser_index](line)
            else:
                if parser_index + 1 < len(line_parsers):
                    parser_index += 1
                yield ""

def parse_grid(file_name, sep="", formatter=int):
    return parse_lines(file_name, line_splitter(sep, formatter))
