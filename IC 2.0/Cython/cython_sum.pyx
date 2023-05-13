def sum_cython(long int n):
	cdef long int i, total = 0
	for i in range(1, n + 1):
		total += i

	return total