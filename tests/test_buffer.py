from telegram_handler.buffer import MessageBuffer

MSG = "abcdefghijk" * 2
MSG_LEN = len(MSG)


def test_sanity():
    buff = MessageBuffer(MSG_LEN + 10)
    buff.write(MSG)
    assert buff.read(MSG_LEN) == MSG


def test_write_out_of_bounds():
    buff = MessageBuffer(MSG_LEN - 10)
    buff.write(MSG)
    assert buff.read(MSG_LEN) == MSG[:-10]


def test_read_out_of_bounds():
    buff = MessageBuffer()
    buff.write(MSG)
    assert buff.read(MSG_LEN + 1) == MSG


def test_write_exact():
    buff = MessageBuffer(MSG_LEN)
    buff.write(MSG)
    assert buff.read(MSG_LEN) == MSG
