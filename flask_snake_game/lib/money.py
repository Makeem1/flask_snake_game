def cents_to_dollars(cents):
	"""
	Convert cent to dollar
	: param cents : Amounts in cents
	: type cenmts : ints
	: return type: flaot
	
	"""

	return round(cents / 100.0, 2)


def dollars_to_cents(dollars):

	"""
	Convert dollar to cents
	: param cents : Amounts in cents
	: type cenmts : ints
	: return type: int
	
	"""

	return int(dollars * 100)

