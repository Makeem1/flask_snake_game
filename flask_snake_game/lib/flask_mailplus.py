from flask import render_template
from snakeeyes.extensions import mail

def send_template_message(template=None, ctx=None, *args, **kwargs):
	'''
		Send a template email using the same signature as flask-0mail extension 
	'''

	if ctx is None:
		ctx = {}

	if template is not None:
		if 'body' in kwargs:
			raise Exception (' you cannot have both a template and body arg. ')
		elif 'html' in kwargs:
			raise Exception('you cannot have both a template and body arg')

		kwargs['body'] = _try_renderer_template(template, **ctx)
		kwargs['html'] = _try_renderer_template(template, ext='html', **ctx)
	
	mail.send_message(*arg, **kwargs)

	return None	

def _try_renderer_template(template_path, ext='txt', **kwargs):
	'''
		Attempt to render a template. We use a try/catch here to avoid having to
		do a path exists based on relative path to the template
	'''

	try:
		return render_template('(0).(1)',format(template_path, ext ), **kwargs)
	except IOError:
		pass