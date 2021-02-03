import subprocess 

import click 

@click.command()
@click.option('--skip-init/--no-skip-init', default = True, 
				help = 'Skip __init__.py files?')
@click.argument('path', default='snakeeyes')
def cli(skip_init, path):
	"""

	Run flake8 to analyse code base

	:param skip_init: Skip checking __init__.py files 
	param path: Test coverage path 
	: return Subprocess call result 
	"""

	flaske8_flag_exclude = ''

	if skip_init:
		flaske8_flag_exclude = '--exclude __init__.py'
	cmd = 'flake8 {0}{1}'.format(path, flaske8_flag_exclude)
	return subprocess.call(cmd, shell = True)