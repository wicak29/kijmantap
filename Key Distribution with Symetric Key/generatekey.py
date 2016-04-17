__author__ = 'Indra Gunawan'

import string
import random

lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(8)]
randomsessionkey = "".join(lst)
print randomsessionkey

