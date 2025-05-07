import sys, re, collections
from typing import Dict, List, Tuple

EDGE_RE = re.compile(r"\s*,\s*")

edges: List[Tuple[int, int, float]] = []
for raw in sys.stdin:
	line = raw.strip()
	if not line:
		continue
	a, b, d = EDGE_RE.split(line)
	edges.append((int(a), int(b), float(d)))

if not edges:
	sys.exit(0)

adj: Dict[int, List[Tuple[int, float]]] = collections.defaultdict(list)
nodes: set[int] = set()
for a, b, w in edges:
	adj[a].append((b, w))
	adj[b].append((a, w))
	nodes.update((a, b))

id2idx = {v: i for i, v in enumerate(sorted(nodes))}
idx2id = {i: v for v, i in id2idx.items()}
n = len(nodes)

best_dist = -1.0
best_state = None
parent: Dict[Tuple[int, int], Tuple[int, int] | None] = {}

if n <= 20:
	from math import inf
	size = 1 << n
	dp = [[-inf] * n for _ in range(size)]
	for i in range(n):
		dp[1 << i][i] = 0.0
		parent[(1 << i, i)] = None
	for mask in range(size):
		for u in range(n):
			dist = dp[mask][u]
			if dist < 0:
				continue
			if dist > best_dist:
				best_dist, best_state = dist, (mask, u)
			for v_id, w in adj[idx2id[u]]:
				v = id2idx[v_id]
				if mask & (1 << v):
					continue
				nmask = mask | (1 << v)
				if dist + w > dp[nmask][v]:
					dp[nmask][v] = dist + w
					parent[(nmask, v)] = (mask, u)
else:
	sys.setrecursionlimit(1 << 25)
	seen: Dict[Tuple[int, int], float] = {}
	def dfs(u, mask, dist):
		global best_dist, best_state
		key = (mask, u)
		if dist <= seen.get(key, -1.0):
			return
		seen[key] = dist
		if dist > best_dist:
			best_dist, best_state = dist, key
		for v_id, w in adj[idx2id[u]]:
			v = id2idx[v_id]
			if mask & (1 << v):
				continue
			parent[(mask | (1 << v), v)] = key
			dfs(v, mask | (1 << v), dist + w)
	for i in range(n):
		dfs(i, 1 << i, 0.0)

mask, cur = best_state
path: List[int] = []
while True:
	path.append(cur)
	prev = parent[(mask, cur)]
	if prev is None:
		break
	mask, cur = prev
for idx in reversed(path):
	print(idx2id[idx])
