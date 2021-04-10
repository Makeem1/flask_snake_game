from flask import jsonify 


def render_json(status, *args, **kwargs):
	"""
	Return a json response 
	Examaple usage:
		render_json(404, {'error' : 'Discount code not found'})
		render_json(200, {'data' : coupon.to_json()})
	"""

	response = jsonify(*args, **kwargs)
	response.status_code = status

	return response 