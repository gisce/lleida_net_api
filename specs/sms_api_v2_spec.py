from lleida_net.sms import SMS_API
import requests


class FakeResponse(object):

    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.payload = payload
        self.content = b''

    def json(self):
        return self.payload


class RecordingSession(object):

    def __init__(self, response):
        self.response = response
        self.calls = []

    def request(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class TimeoutSession(object):

    def request(self, **kwargs):
        raise requests.exceptions.Timeout('timed out')


with description('SMS API compatibility'):

    with it('preserves the 0.6.2 request by default'):
        api = SMS_API(user='legacy-user', password='legacy-password')
        session = RecordingSession(FakeResponse(
            200, {'code': 200, 'status': 'Success', 'request': 'sms'}
        ))
        api.session = session

        response = api.post('', json={'sms': {'txt': 'hello'}})
        request = session.calls[0]

        assert response.error is False
        assert request['json']['sms']['user'] == 'legacy-user'
        assert request['json']['sms']['password'] == 'legacy-password'
        assert 'Authorization' not in request['headers']
        assert 'timeout' not in request

    with it('uses API key options without leaking it into the payload'):
        api = SMS_API(
            user='api-user',
            password='api-key',
            api_key='api-key',
            api_url='https://sms.example.test/v2',
            timeout=15,
            preserve_error_response=True,
        )
        session = RecordingSession(FakeResponse(
            200, {
                'code': 1504,
                'status': 'Temporary error',
                'request': 'sms',
            }
        ))
        api.session = session

        response = api.post('', json={'sms': {'txt': 'hello'}})
        request = session.calls[0]

        assert response.error is True
        assert response.result['code'] == 1504
        assert request['url'] == 'https://sms.example.test/v2/'
        assert request['headers']['Authorization'] == 'x-api-key api-key'
        assert request['timeout'] == 15
        assert request['json']['sms']['user'] == 'api-user'
        assert 'password' not in request['json']['sms']

    with it('captures transport errors only when explicitly requested'):
        api = SMS_API(
            user='api-user',
            password='api-key',
            capture_transport_errors=True,
        )
        api.session = TimeoutSession()

        response = api.post('', json={'sms': {'txt': 'hello'}})

        assert response.error is True
        assert response.transport_error == 'timeout'
        assert response.result == {}
