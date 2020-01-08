from decimal import *


class ARC4:
    code_table_encrypt = [40, 83, 235, 20, 225, 118, 1, 60, 229, 51, 23, 107, 204, 98, 150, 15, 184, 24, 140, 79, 55,
                          87, 10, 191, 99, 70, 109, 227, 66, 149, 172, 217, 86, 247, 137, 38, 0, 200, 5, 143, 151, 131,
                          144, 64, 224, 197, 127, 123, 187, 236, 201, 218, 126, 244, 11, 101, 16, 44, 26, 181, 110, 124,
                          94, 206, 54, 136, 34, 243, 42, 165, 228, 215, 176, 56, 9, 115, 209, 245, 202, 164, 231, 147,
                          3, 159, 248, 145, 139, 82, 30, 171, 168, 198, 242, 166, 116, 78, 95, 233, 162, 80, 199, 189,
                          146, 67, 104, 160, 234, 17, 97, 129, 114, 57, 113, 188, 190, 133, 31, 22, 153, 253, 100, 205,
                          208, 76, 180, 246, 112, 161, 221, 8, 61, 178, 154, 75, 117, 28, 49, 121, 237, 29, 74, 50, 53,
                          62, 96, 185, 210, 222, 119, 33, 13, 120, 12, 111, 216, 32, 39, 173, 71, 230, 251, 141, 128,
                          47, 241, 43, 207, 108, 179, 68, 196, 148, 193, 142, 81, 37, 192, 48, 183, 130, 77, 102, 211,
                          203, 232, 59, 156, 35, 105, 135, 19, 226, 93, 41, 167, 212, 65, 186, 69, 195, 21, 134, 45,
                          220, 194, 155, 157, 7, 170, 182, 36, 63, 4, 213, 249, 92, 14, 84, 125, 2, 158, 214, 103, 46,
                          254, 163, 72, 85, 175, 169, 25, 138, 177, 255, 239, 132, 18, 73, 238, 90, 240, 88, 89, 250,
                          52, 6, 219, 174, 91, 58, 152, 252, 223, 27, 122, 106]
    code_table_decrypt = None
    key = None
    key_number = None
    length_sequence = None
    sequence = None
    generator_sequence = None

    def __init__(self, key):
        self.key = key
        self.key_number = self._key_to_number()
        self.length_sequence = 1024 * 1 * 2 + 1024  # для (size * 2)кб + 1кб для генерации ключа ключа
        self.sequence = self.generate_sequence_numbers_sqrt()
        self.generator_sequence = self._get_pair_seq(self.sequence[1024:], 2)
        self.generate_new_tables()

    def encode(self, code: int):
        key_code = next(self.generator_sequence, None)
        if key_code is None:
            self._update_sequence()
            key_code = next(self.generator_sequence, None)
        return self.code_table_encrypt[(code ^ int(key_code))]

    def decode(self, code: int):
        key_code = next(self.generator_sequence, None)
        if key_code is None:
            self._update_sequence()
            key_code = next(self.generator_sequence, None)
        return self.code_table_decrypt[code] ^ int(key_code)

    def generate_new_tables(self):
        sequence_numbers = self._get_pair_seq(self.sequence[:1024], 4)
        table = list(range(256))
        table_cur = list(range(256))
        table_code = list()
        for i in range(256):
            code = next(sequence_numbers, None)
            index = 16 * (int(code[:2]) % 16) + (int(code[-2:]) % 16)
            cur_val = table[index]
            if cur_val is None:
                val = table_cur[index % len(table_cur)]
                table_code.append(val)
                table_cur.remove(val)
                table[val] = None
            else:
                table_code.append(cur_val)
                table_cur.remove(cur_val)
                table[index] = None
        self.code_table_encrypt = table_code
        self.code_table_decrypt = [table_code.index(i) for i in range(256)]

    def _key_to_number(self):
        code_letters = [str(self.code_table_encrypt[ord(symbol) % 256]) for symbol in self.key]
        return int("".join(code_letters))

    def generate_sequence_numbers_sqrt(self):
        getcontext().prec = self.length_sequence
        sequence = Decimal(self.key_number).sqrt()
        sequence = str(sequence).replace('.', '')
        if len(sequence) < self.length_sequence:
            sequence = Decimal(self.key_number + 1).sqrt()
            sequence = str(sequence).replace('.', '')
        return sequence

    @staticmethod
    def _get_pair_seq(seq, len_pair):
        count_pair = len(seq) // len_pair
        for ind in range(count_pair):
            yield seq[ind * len_pair:ind * len_pair + len_pair]

    def _update_sequence(self):
        self.key_number = self._key_to_number()
        self.sequence = self.generate_sequence_numbers_sqrt()
        self.generator_sequence = self._get_pair_seq(self.sequence[1024:], 2)
        self.generate_new_tables()
