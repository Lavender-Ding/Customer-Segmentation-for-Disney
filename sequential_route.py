# -*- coding: cp936 -*-


def route_extract(route, spot_set):
    ans = [route[ii] for ii in xrange(len(route)) 
            if (not route[ii] in route[:ii]) and route[ii] in spot_set]
    if len(ans) != len(spot_set): return False
    return ans
    
    
def count_table(content):
    ans = dict()
    for ii in content:
        ans[ii] = ans.get(ii, 0) + 1
    return ans
    

def sequential_route_construct(content, spot_set, min_support = False):
        
    route_content = []
    for line in content:
        tmp_ans = route_extract(line, spot_set)
        if tmp_ans:
            route_content.append(tuple(tmp_ans)) 
    
    ans = count_table(route_content)
    
    if min_support:
        tmp_ans = dict()
        if min_support < 1:
            min_support = len(content) * min_support
        for ii in ans:
            if ans[ii] >= min_support:
                tmp_ans[ii] = ans[ii]
        ans = tmp_ans
    
    return ans



