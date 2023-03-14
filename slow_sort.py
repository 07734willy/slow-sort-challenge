"""
Sorts elements of a list by representing the numbers as rings on a pillar in
the game "Tower of Hanoi", and naively brute-forcing a solution
"""
import time


def is_valid(stack, value):
	"""
	Checks that adding :value: to the top of the stack :stack: doesn't violate
	the rules of Tower of Hanoi (one cannot place a larger value/ring directly
	ontop of a smaller value/ring)
	"""
	return not stack or value <= stack[0]


def push(a, b, c, depth, value):
	"""
	Attempts to place the value/ring :value: on the top of each stack :a:, :b:,
	and :c:, in turn, and mutually recurses on `pop`
	"""
	if is_valid(a, value):
		yield from pop([value] + a, b, c, depth - 1)
	if is_valid(b, value):
		yield from pop(a, [value] + b, c, depth - 1)
	if is_valid(c, value):
		yield from pop(a, b, [value] + c, depth - 1)


def pop(a, b, c, depth):
	"""
	Attempts to remove the top value/ring from each stack :a:, :b:, and :c: in
	turn, and mutually recurses on `push`. If at any point all the values/rings
	are moved onto the :c: stack, a solution has been found and is yielded.
	The recursion is terminated with the depth :depth: is reached.
	"""
	if not a and not b:
		yield c
	if not depth:
		return

	if a:
		yield from push(a[1:], b, c, depth, a[0])
	if b:
		yield from push(a, b[1:], c, depth, b[0])
	if c:
		yield from push(a, b, c[1:], depth, c[0])


def iddfs(values, depth=1):
	"""
	Implements Iterative Deepening Depth-First Search over the solution space
	of "Towers of Hanoi". A DFS of fixed depth is performed at each iteration,
	in increasing depth, until a solution is found.
	"""
	for retval in pop(values, [], [], depth):
		return retval
	return iddfs(values, depth + 1)


def slow_sort(numbers: list) -> None:
	numbers[:] = iddfs(numbers)


if __name__ == '__main__':
	numbers = list(map(int, input("Space delimited list: ").split()))

	start_time = time.time_ns() / 1000000
	slow_sort(numbers)
	end_time = time.time_ns() / 1000000
	
	print(f'Elapsed time: {end_time - start_time} milliseconds.')
