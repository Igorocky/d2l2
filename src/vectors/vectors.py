import math
import random


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


def make_random_versions(init: list[list[int]], num_of_versions: int) -> list[list[list[int]]]:
    res = []
    for i in range(num_of_versions):
        new_grp = []
        for vec in init:
            idx1 = random.randint(0,len(vec)-1)
            idx2 = random.randint(0,len(vec)-1)
            new_vec = vec.copy()
            tmp = new_vec[idx1]
            new_vec[idx1] = new_vec[idx2]
            new_vec[idx2] = tmp
            new_grp.append(new_vec)
        res.append(new_grp)
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

def main() -> None:
    max_dist = 0.0
    max_grps:list[list[list[int]]] = []
    grp = [list(range(1,7)) for i in range(8)]
    print('------------------------------------')
    print(f'epoch=0')
    print(f'dist={dist_all(grp)}')
    print(f'{grp=}')
    for epoch in range(1,100_000+1):
        grp = select_max(make_random_versions(grp, 100))
        dist = dist_all(grp)
        if dist > max_dist:
            max_dist = dist
            max_grps = [grp]
        elif dist == max_dist:
            max_grps.append(grp)
        print('------------------------------------')
        print(f'{epoch=}')
        print(f'dist={dist_all(grp)}')
        print(f'{grp=}')
    print('====================================')
    print(f'{max_dist=}')
    print(f'{max_grps=}')


if __name__ == '__main__':
    main()
