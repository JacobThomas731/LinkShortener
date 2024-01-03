class ShorteningAlgo:

    def __init__(self):
        self.l1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.l2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v',
                   'w',
                   'x', 'y', 'z']
        self.l3 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V',
                   'W',
                   'X', 'Y', 'Z']

    def next_value(self, val):
        last_digit = val[-1]
        if not last_digit or last_digit in '9zZ':
            if last_digit == '9':
                return val[:-1] + 'A'
            elif last_digit == 'Z':
                return val[:-1] + 'a'
            else:
                for i, s in enumerate(val[::-1]):
                    if s != 'z':
                        return self.next_value(val[:len(val) - i]) + '0' * i
                    else:
                        pass
                return '0' * (len(val) + 1)

        else:
            if last_digit in self.l1:
                new_val = self.l1[self.l1.index(last_digit) + 1]
                return val[:-1] + new_val
            elif last_digit in self.l2:
                new_val = self.l2[self.l2.index(last_digit) + 1]
                return val[:-1] + new_val
            else:
                new_val = self.l3[self.l3.index(last_digit) + 1]
                return val[:-1] + new_val


