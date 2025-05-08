import sys


keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def solve(data):
    from collections import deque
    import heapq

    h = len(data)
    w = len(data[0]) if h > 0 else 0
    starts = []
    key_positions = {}
    for i in range(h):
        for j in range(w):
            c = data[i][j]
            if c == '@':
                starts.append((i, j))
            elif c in keys_char:
                key_positions[c] = (i, j)
    starts.sort()
    K = len(key_positions)
    if K == 0:
        return 0

    keys_sorted = sorted(key_positions.keys())
    key_index = {c: idx for idx, c in zip(range(len(keys_sorted)), keys_sorted)}
    adjacency = {node: [] for node in range(K + len(starts))}

    def bfs_from(r0, c0):
        visited = {}
        dq = deque()
        dq.append((r0, c0, 0, 0))
        visited[(r0, c0)] = [0]
        edges = []
        while dq:
            r, c, req_mask, dist = dq.popleft()
            ch = data[r][c]
            if ch in keys_char:
                kidx = key_index[ch]
                if dist > 0:
                    edges.append((kidx, dist, req_mask))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < h and 0 <= nc < w):
                    continue
                ch2 = data[nr][nc]
                if ch2 == '#':  # стена
                    continue
                new_mask = req_mask
                if ch2 in doors_char:
                    keychar = ch2.lower()
                    if keychar in key_index:
                        new_mask |= (1 << key_index[keychar])
                    else:
                        continue
                state = (nr, nc)
                if state not in visited:
                    visited[state] = [new_mask]
                else:
                    skip = False
                    to_remove = []
                    for m in visited[state]:
                        if (m & new_mask) == m:
                            skip = True
                            break
                        if (new_mask & m) == new_mask:
                            to_remove.append(m)
                    if skip:
                        continue
                    for m in to_remove:
                        visited[state].remove(m)
                    visited[state].append(new_mask)
                dq.append((nr, nc, new_mask, dist + 1))
        return edges

    for c, (kr, kc) in key_positions.items():
        kidx = key_index[c]
        for (dest_k, dist, req) in bfs_from(kr, kc):
            if dest_k != kidx:
                adjacency[kidx].append((dest_k, dist, req))
    for i in range(len(starts)):
        sr, sc = starts[i]
        start_idx = K + i
        for (dest_k, dist, req) in bfs_from(sr, sc):
            adjacency[start_idx].append((dest_k, dist, req))

    full_mask = (1 << K) - 1
    initial_positions = tuple(K + i for i in range(len(starts)))
    pq = [(0, 0, initial_positions)]  # (cost, mask, (pos0,pos1,pos2,pos3))
    visited_states = {(0, initial_positions): 0}
    while pq:
        cost, mask, positions = heapq.heappop(pq)
        if visited_states.get((mask, positions), float('inf')) < cost:
            continue
        if mask == full_mask:
            return cost
        for i in range(len(positions)):
            pos = positions[i]
            for (next_k, dist, req) in adjacency[pos]:
                if (mask >> next_k) & 1:
                    continue
                if (req & ~mask) != 0:
                    continue
                new_mask = mask | (1 << next_k)
                new_cost = cost + dist
                new_positions = list(positions)
                new_positions[i] = next_k
                new_positions = tuple(new_positions)
                prev_cost = visited_states.get((new_mask, new_positions), float('inf'))
                if new_cost < prev_cost:
                    visited_states[(new_mask, new_positions)] = new_cost
                    heapq.heappush(pq, (new_cost, new_mask, new_positions))
    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)

if __name__ == '__main__':
    main()
