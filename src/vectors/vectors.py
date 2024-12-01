import math
import random
from random import shuffle


def dist(a: list[int], b: list[int]) -> float:
    sum_ = 0
    for i in range(len(a)):
        sum_ += (a[i] - b[i]) ** 2
    return math.sqrt(sum_)


def dist_all(vectors: list[list[int]]) -> float:
    res = 0.0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            res += dist(vectors[i], vectors[j])
    return res

def has_correct_corner_counts(grp:list[list[int]], max_corner_cnt:int) -> bool:
    counts:dict[int,int] = {}
    def inc_cnt(n:int) -> bool:
        if n not in counts:
            counts[n] = 0
        counts[n] += 1
        return counts[n] <= max_corner_cnt
    for v in grp:
        if not inc_cnt(v[0]):
            return False
        if not inc_cnt(v[-1]):
            return False
    return True


def make_random_versions(init: list[list[int]], num_of_versions: int, max_corner_cnt:int) -> list[list[list[int]]]:
    res = []
    for i in range(num_of_versions):
        new_grp = []
        for vec in init:
            # idx1 = random.randint(0,len(vec)-1)
            # idx2 = random.randint(0,len(vec)-1)
            new_vec = vec.copy()
            shuffle(new_vec)
            # tmp = new_vec[idx1]
            # new_vec[idx1] = new_vec[idx2]
            # new_vec[idx2] = tmp
            new_grp.append(new_vec)
        if has_correct_corner_counts(new_grp, max_corner_cnt):
            res.append(new_grp)
    if len(res) == 0:
        res.append(init)
    return res

def select_max(grps:list[list[list[int]]]) -> list[list[int]]:
    max_grp = grps[0]
    max_dist = dist_all(max_grp)
    for i in range(1,len(grps)):
        new_grp = grps[i]
        new_dist = dist_all(new_grp)
        if max_dist < new_dist:
            max_dist = new_dist
            max_grp = new_grp
    return max_grp

def vec_to_str(vec:list[int]) -> str:
    return ''.join(str(v) for v in vec)

def grp_to_str(grp:list[list[int]]) -> str:
    res = [vec_to_str(v) for v in grp]
    res.sort()
    return ' '.join(res)

def main() -> None:
    vec_len = 6
    num_of_vec = 12
    num_of_epochs = 100_000
    max_num_of_rand_versions = 100
    max_dist = 0.0
    max_grps:set[str] = set()
    grp = [list(range(1,vec_len+1)) for i in range(num_of_vec)]
    max_corner_cnt = math.ceil(num_of_vec*2/vec_len)
    print('------------------------------------')
    print(f'epoch=0')
    print(f'dist={dist_all(grp)}')
    print(f'{grp=}')
    for epoch in range(1,num_of_epochs+1):
        grp = select_max(make_random_versions(grp, num_of_versions=max_num_of_rand_versions, max_corner_cnt=max_corner_cnt))
        dist = dist_all(grp)
        if dist > max_dist:
            max_dist = dist
            max_grps = set()
        if dist == max_dist:
            max_grps.add(grp_to_str(grp))
        print('------------------------------------')
        print(f'{epoch=}')
        print(f'dist={dist_all(grp)}')
        print(f'{grp=}')
    print('====================================')
    print(f'{max_corner_cnt=}')
    print(f'{max_dist=}')
    max_grps_strs = list(max_grps)
    max_grps_strs.sort()
    print('max_grps:')
    for g in max_grps_strs:
        print(g)


if __name__ == '__main__':
    main()
