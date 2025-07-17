timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:05] "GET /settings HTTP/1.0" 200 -
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:05] "GET /static/style.css HTTP/1.0" 304 -
timetracker    | [2025-07-17 14:36:07,229] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:07] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:09,235] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:09] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:09,803] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:09] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:10,012] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:10] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:10,216] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:10] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:10,405] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:10] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:36:10,614] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 47, in index
timetracker    |     data = load_json(TRACK_FILE, {})
timetracker    |   File "/app/app.py", line 34, in load_json
timetracker    |     return json.load(f)
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 293, in load
timetracker    |     return loads(fp.read(),
timetracker    |   File "/usr/local/lib/python3.10/json/__init__.py", line 346, in loads
timetracker    |     return _default_decoder.decode(s)
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
timetracker    |     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
timetracker    |   File "/usr/local/lib/python3.10/json/decoder.py", line 355, in raw_decode
timetracker    |     raise JSONDecodeError("Expecting value", s, err.value) from None
timetracker    | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
timetracker    | 172.19.0.1 - - [17/Jul/2025 14:36:10] "GET / HTTP/1.0" 500 -
