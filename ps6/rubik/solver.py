import rubik
import pdb 

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    #raise NotImplementedError

    if start == end:
        return []

    try:
        x = bfs(start)
        y = bfs(end)

        k = 0
        while k < 8:
            a_levels = x.next()
            b_levels = y.next()

            if a_levels > 1:
                t = [(-1, -2), (-2, -1), (-1, -1)]
            else:
                t = [(-1, -1)]

            for (i, j) in t: 
                common = compare_levels(a_levels[i], b_levels[j])
                if common:
                    return construct_path(a_levels, i, b_levels, j, common)

            k += 1

        return None
                    
    except StopIteration:
        return None

def compare_levels(a_level, b_level):
    for a in a_level:
            if a in b_level:
                return a
    return None
     
def construct_path(a_levels, i, b_levels, j, common):
    l = []
    x = common
    for i in range(len(a_levels) + i, 0, -1): 
        val = a_levels[i][x] 
        x = val[0]
        l.append(val[1])

    l.reverse()
    #l.append(common[1])

    x = common
    for i in range(len(b_levels) + j, 0, -1): 
        val = b_levels[i][x] 
        x = val[0]
        l.append(rubik.perm_inverse(val[1]))

    return l


def bfs(start):
    nxt = {start: None}
    levels = [nxt]

    while levels[-1]:
        nxt = {}
        for s in levels[-1]:
            #for p in generate_positions(s):
            #pdb.set_trace()
            for perm in rubik.quarter_twists:
                p = rubik.perm_apply(perm, s)
                if p not in levels[-1] and (len(levels) <= 1 or p not in levels[-2]):  
                    nxt[p] = (s, perm, rubik.quarter_twists_names[perm]) #value is a parent. duplicates are overwritten, 
                    #since it is a dictionary
                    #+ record a move
        levels.append(nxt)
        yield levels

#def generate_positions(start):
#    """
#    Returns a list of new positions applied to 'start' position 
#    by executing all possible quarter twists
#    """
#
#    return [rubik.perm_apply(perm, start) for perm in rubik.quarter_twists]


    
