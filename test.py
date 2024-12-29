import utils


def test_is_command():
    is_command = utils.is_command

    def assert_command(msg, expected):
        ok, cmd, args = is_command(msg)
        assert ok == expected
        if ok:
            print(msg, ok, cmd, args)
            # print("cmd==>", cmd())

    assert_command('', False)
    assert_command(' ', False)
    assert_command('/ls', True)
    assert_command(' /ls', False)
    assert_command('/ls ', True)
    assert_command('   /ls  ', False)
    assert_command('/lss', False)
    assert_command('/ls sss', True)


test_is_command()
