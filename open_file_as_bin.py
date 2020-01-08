from RC4 import ARC4


class ShiftOne:

    @staticmethod
    def encode(code: int):
        return (code + 1) % 256

    @staticmethod
    def decode(code: int):
        return (code - 1) % 256


def encode_file(src, out, class_crypt, chank_size=64):
    with open(src, "br") as bin_file, open(out, "bw") as write_bin:
        while True:
            line = bin_file.read(chank_size)
            bline = bytearray(line)
            for i in range(len(bline)):
                bline[i] = class_crypt.encode(bline[i])
            write_bin.write(bline)
            if not line:
                break


def decode_file(src, out, class_crypt, chank_size=64):
    with open(src, "br") as bin_file, open(out, "bw") as write_bin:
        while True:
            line = bin_file.read(chank_size)
            bline = bytearray(line)
            for i in range(len(bline)):
                bline[i] = class_crypt.decode(bline[i])
            write_bin.write(bline)
            if not line:
                break


if __name__ == "__main__":
    test = True
    if test:
        # test txt
        rc4 = ARC4("keyword")
        encode_file(r"test\text\test_lit.txt", r"test\text\encrypt", rc4)
        rc4 = ARC4("keyword")
        decode_file(r"test\text\encrypt", r"test\text\test_lit_copy.txt", rc4)
        # test pdf
        rc4 = ARC4("keyword")
        encode_file(r"test\pdf\byte_of_python.pdf", r"test\pdf\encrypt", rc4)
        rc4 = ARC4("keyword")
        decode_file(r"test\pdf\encrypt", r"test\pdf\byte_of_python_copy.pdf", rc4)
        # test zip
        rc4 = ARC4("keyword")
        encode_file(r"test\zip\test_lit.zip", r"test\zip\encrypt", rc4)
        rc4 = ARC4("keyword")
        decode_file(r"test\zip\encrypt", r"test\zip\test_lit_copy.zip", rc4)



