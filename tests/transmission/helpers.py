#!.env/bin/python
# flake8: noqa

def sample_request_session_id():
    class MockRequest:
        def __init__(self):
            self.text = sample_session_id()

        def __getattr__(self, attr):
            if attr not in self.__dict__:
                self.__dict__[attr] = None

            return self.__dict__[attr]

    return MockRequest()

def sample_session_id():
    return '<h1>409: Conflict</h1><p>Your request had an invalid session-id header.</p><p>To fix this, follow these steps:<ol><li> When reading a response, get its X-Transmission-Session-Id header and remember it<li> Add the updated header to your outgoing requests<li> When you get this 409 error message, resend your request with the updated header</ol></p><p>This requirement has been added to help prevent <a href="https://en.wikipedia.org/wiki/Cross-site_request_forgery">CSRF</a> attacks.</p><p><code>X-Transmission-Session-Id: xzlXm3vehtAlAJVOim481B4pb2l6yfBVYQZPq0dDqoaw8U6g</code></p>'