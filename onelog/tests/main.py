import mock
import unittest

from onelog import OneLog as OL


class OneLogTester(unittest.TestCase):

    def test_get_log_data(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        assert(log_data.path == 'onelog.test')
        assert(log_data.method == 'test_get_log_data')
        assert(log_data.state == OL.START)
        assert(log_data.data == {})

    def test_get_log_data_set_data(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data',
                                   data={'state_msg': 'started'})

        assert(log_data.path == 'onelog.test')
        assert(log_data.method == 'test_get_log_data')
        assert(log_data.data == {'state_msg': 'started'})

    def test_fail_log_data(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        data = OL.fail(log_data)
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.FAILURE)
        assert(data.data == {})

    def test_fail_log_data_update(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        data = OL.fail(log_data, data={'state_msg': 'we failed'})
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.FAILURE)
        assert(data.data == {'state_msg': 'we failed'})

    def test_success_log_data(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        data = OL.succeed(log_data)
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.SUCCESS)
        assert(data.data == {})

    def test_success_log_data_update(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data',
                                   data={})

        data = OL.succeed(log_data, data={'state_msg': 'we succeeded'})
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.SUCCESS)
        assert(data.data == {'state_msg': 'we succeeded'})

    def test_log_data_update(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data',
                                   data={})

        data = OL.update(log_data, data={'state_msg': 'updated'})
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.START)
        assert(data.data == {'state_msg': 'updated'})

    def test_log_data_deep_update(self):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data',
                                   data={"animals": {
                                       "dog": {"owner": "me"},
                                       "cat": {"owner": "you"}}})

        data = OL.update(log_data, data={"animals": {"dog": {"owner": "you"}}})
        assert(data.path == 'onelog.test')
        assert(data.method == 'test_get_log_data')
        assert(data.state == OL.START)
        assert(data.data['animals']['dog'] == {"owner": "you"})
        assert(data.data['animals']['cat'] == {"owner": "you"})

    @mock.patch('onelog.log.info')
    def test_log_info(self, log_mock):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data',
                                   data={})

        assert(log_data.path == 'onelog.test')
        assert(log_data.method == 'test_get_log_data')
        assert(log_data.state == OL.START)
        assert(log_data.data == {})

        OL.info(log_data)

        log_mock.assert_called_with({'path': 'onelog.test',
                                     'state': 'log_data.state',
                                     'method': 'test_get_log_data',
                                     'state': 'START',
                                     'data': {}})

    @mock.patch('onelog.log.exception')
    def test_log_exception(self, log_mock):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        assert(log_data.path == 'onelog.test')
        assert(log_data.method == 'test_get_log_data')
        assert(log_data.state == OL.START)
        assert(log_data.data == {})

        OL.exception(OL.fail(log_data))

        log_mock.assert_called_with({'path': 'onelog.test',
                                     'state': 'log_data.state',
                                     'method': 'test_get_log_data',
                                     'state': 'FAILURE',
                                     'data': {}})

    @mock.patch('onelog.log.error')
    def test_log_error(self, log_mock):
        log_data = OL.get_log_data('onelog.test',
                                   'test_get_log_data')

        assert(log_data.path == 'onelog.test')
        assert(log_data.method == 'test_get_log_data')
        assert(log_data.state == OL.START)
        assert(log_data.data == {})

        OL.error(OL.fail(log_data))

        log_mock.assert_called_with({'path': 'onelog.test',
                                     'state': 'log_data.state',
                                     'method': 'test_get_log_data',
                                     'state': 'FAILURE',
                                     'data': {}})
