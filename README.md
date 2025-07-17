timetracker    | 172.19.0.1 - - [17/Jul/2025 14:41:25] "GET / HTTP/1.0" 500 -
timetracker    | [2025-07-17 14:41:25,366] ERROR in app: Exception on / [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 90, in index
timetracker    |     start_time=start_dt.strftime("%Y-%m-%d %H:%M:%S"),
timetracker    | UnboundLocalError: local variable 'start_dt' referenced before assignment
