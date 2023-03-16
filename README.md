# The Challenge

This is my submission for the [slowest sorting algorithm challenge](https://github.com/Tom3s/slow-sort-challenge). 

The rules, in a nutshell- the algorithm must be deterministic, and each operation must make progress towards a solution (no pointless computations).

### My Approach

I've based my sorting algorithm off of the game [Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi). The can be summarized as below:

- You have three pillars, and many different sized rings
- The rings start on the left-most pillar, and must be moved to the right-most pillar
- You can only move one ring at a time
- A larger ring cannot be placed directly ontop of a smaller ring.

In the actual game, the rings start off in non-decreasing size, from top to bottom, on the left pillar. However, the game is still playable even if this is not scenario, as is the case in the sorting algorithm. It just means that we can only restrict the ring sizes with respect to the topmost element on each pillar.

Once the game completes, all the rings will be on the right-most pillar, and due to the size constraint, they will be ordered in non-decreasing size. This means we can sort the rings by winning the game. 

*Disclaimer*: The observation that playing the Tower of Hanoi game on unsorted rings has the side effect of sorting the rings is not my own- I read it somewhere online, but the author had neglected to bring the idea to fruition in the form of a stand-alone sorting algorithm. A number of years ago, I took the idea, and implemented it in a horrific brute-force algorithm, with the intent of creating the world's worst deterministic sorting algorithm. The algorithm I've provided in this repo is a cleaned up version of that code. Unfortunately, I've lost the original article that sparked the original idea. If anyone happens to stumble upon it, I'll happily add it as a reference here.

### Time Complexity

The minimal number of moves to solve a normal Tower of Hanoi game of `N` rings is `2^N-1`. Any inversions introduced into the left-most pillar will actually **decrease** this lower bound. This means means a recursive search of the solution space will have depth `O(2^N)`. By naively attempting every valid pop/push sequence, we end up with a worst-case branching factor of `9` (`3` from-pillars, `3` to-pillars). In practice, many of the pop/push combinations will be invalid (putting a larger ring ontop of a smaller ring), so some nodes in the search tree may have a branching factor less than `9`. However, there will almost always be at least one ring on each pillar, so we can almost always pop from each pillar. Unless we're on the left-most pillar, we're guaranteed that the we push the ring back onto the pillar that it was popped from. If the ring is the smallest of the topmost rings across the 3 pillars, it will also be able to be placed ontop of either of the other two. If the ring is the second smallest, it will be able to be placed ontop of the 3rd smallest. 

This means there's typically going to be either 5 or 6 valid pop/push moves (depending whether the ring on the left-most pillar can be placed back onto its same pillar), and occassionally more, up to 9, when there's duplicate sized rings. However, for what difficulty duplicates pose in branching, they compensate in search depth- its much, much faster to solve an Tower of Hanoi problem with duplicates than one of equal size without duplicates, so for the sake of simplicity of the worst-case time analysis, we'll assume the input is free of duplicates.

This gives a starting complexity of a fixed-depth search as `O(6^(2^N))`. Each of these involve `O(N)` work (copying the stack-to-mutate). We do an iterative deepening depth-first search, from depth `1` to `N`, however due to the exponential nature of the search space, the deepest search alone dominates the complexity. This brings us to a total time complexity of `O(N * 6^(2^N))`.


### Runtime

This algorithm is incredibly slow. Its slowest for values sorted in non-descending order, and fastest for non-increasing order. 

For sorting three elements:
```
Space delimited list: 1 2 3
Elapsed time: 16.1181640625 milliseconds.
```
For sorting four elements:
```
Space delimited list: 1 2 3 4
Elapsed time: 5850997.044677734 milliseconds.

```
-which is about 1.6 hours.
