def generate_verilog_code(pixels):
    binary = dict()

    for pixel, data in enumerate(pixels):
        if not (data[0] == 0 and data[1] == 0 and data[2] == 0):
            red = '{0:05b}'.format(data[0] // 8)
            green = '{0:06b}'.format(data[1] // 4)
            blue = '{0:05b}'.format(data[2] // 8)

            color = (red + green + blue)
            assert len(color) == 16
            if color not in binary:
                binary[color] = [pixel]
            else:
                binary[color].append(pixel)

    def interval_extract(lst):
        lst = sorted(set(lst))
        range_start = previous_number = lst[0]

        for number in lst[1:]:
            if number == previous_number + 1:
                previous_number = number
            else:
                yield [range_start, previous_number]
                range_start = previous_number = number
        yield [range_start, previous_number]

    verilog_code = ""

    for i, color in enumerate(binary):
        if i != 0:
            verilog_code += 'else if ('
            pixel_ranges = list(interval_extract(binary[color]))
            for j, pixel_range in enumerate(pixel_ranges):
                if j != len(pixel_ranges) - 1:
                    if pixel_range[0] == pixel_range[1]:
                        verilog_code += f'pixel_index == {pixel_range[0]} || '
                    else:
                        verilog_code += f'((pixel_index >= {pixel_range[0]}) && (pixel_index <= {pixel_range[1]})) || '
                else:
                    if pixel_range[0] == pixel_range[1]:
                        verilog_code += f'pixel_index == {pixel_range[0]})'
                    else:
                        verilog_code += f'(pixel_index >= {pixel_range[0]}) && (pixel_index <= {pixel_range[1]}))'
            verilog_code += f" oled_data = 16'b{color};\n"
        else:
            verilog_code += 'if ('
            pixel_ranges = list(interval_extract(binary[color]))
            for j, pixel_range in enumerate(pixel_ranges):
                if j != len(pixel_ranges) - 1:
                    if pixel_range[0] == pixel_range[1]:
                        verilog_code += f'pixel_index == {pixel_range[0]} || '
                    else:
                        verilog_code += f'((pixel_index >= {pixel_range[0]}) && (pixel_index <= {pixel_range[1]})) || '
                else:
                    if pixel_range[0] == pixel_range[1]:
                        verilog_code += f'pixel_index == {pixel_range[0]})'
                    else:
                        verilog_code += f'(pixel_index >= {pixel_range[0]}) && (pixel_index <= {pixel_range[1]}))'
            verilog_code += f" oled_data = 16'b{color};\n"

    verilog_code += "else oled_data = 0;\n"

    return verilog_code
