from secrets import token_hex

import click 

@click.command()
def cli():
	"""Generating secure token."""

	return click.echo(token_hex(32))