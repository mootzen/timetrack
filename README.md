# timetrack
timetracker    | 172.19.0.1 - - [17/Jul/2025 13:30:37] "POST /start HTTP/1.0" 302 -
timetracker    | 172.19.0.1 - - [17/Jul/2025 13:30:37] "GET / HTTP/1.0" 200 -
timetracker    | 172.19.0.1 - - [17/Jul/2025 13:30:37] "GET /static/style.css HTTP/1.0" 304 -
timetracker    | [2025-07-17 13:30:38,523] ERROR in app: Exception on /history [GET]
timetracker    | Traceback (most recent call last):
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1511, in wsgi_app
timetracker    |     response = self.full_dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 919, in full_dispatch_request
timetracker    |     rv = self.handle_user_exception(e)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 917, in full_dispatch_request
timetracker    |     rv = self.dispatch_request()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 902, in dispatch_request
timetracker    |     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
timetracker    |   File "/app/app.py", line 131, in history
timetracker    |     return render_template('history.html', entries=entries)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/templating.py", line 150, in render_template
timetracker    |     return _render(app, template, context)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/flask/templating.py", line 131, in _render
timetracker    |     rv = template.render(context)
timetracker    |   File "/usr/local/lib/python3.10/site-packages/jinja2/environment.py", line 1295, in render
timetracker    |     self.environment.handle_exception()
timetracker    |   File "/usr/local/lib/python3.10/site-packages/jinja2/environment.py", line 942, in handle_exception
timetracker    |     raise rewrite_traceback_stack(source=source)
timetracker    |   File "/app/templates/history.html", line 26, in top-level template code
timetracker    |     {% for week, total in weekly_summary.items() %}
timetracker    |   File "/usr/local/lib/python3.10/site-packages/jinja2/environment.py", line 490, in getattr
timetracker    |     return getattr(obj, attribute)
timetracker    | jinja2.exceptions.UndefinedError: 'weekly_summary' is undefined
timetracker    | 172.19.0.1 - - [17/Jul/2025 13:30:38] "GET /history HTTP/1.0" 500 -
