import collections

def get_fieldsets_strings(l):
	#lookup on all the structer of the fieldsets for the strings on it
	if not isinstance(l, collections.Iterable): return []
	res = []
	for e in l:
		if isinstance(e, str): res.append(e)
		elif isinstance(e, dict): 
			for key, item in e.items(): 
				res += get_fieldsets_strings(item)
		else: 
			res += get_fieldsets_strings(e)
	return res
