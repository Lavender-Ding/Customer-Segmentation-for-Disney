# -*- coding: gb2312 -*-


from operator import itemgetter


def read_route(filename="外地个体构造表.txt", filter=None, by="id", id_list=False, date_range="all", min_length=False):
    
    ans = []
    
    with open(filename, "r") as ff:
        content = [line.strip().split("\t") for line in ff]
    
    D_spot_category = spot_category_read(filename = "spot_category.csv")    
    
    error_key = []
    for line in content:
        
        if id_list:
            if not line[0] in id_list:
                continue

        tmp_ans = dict()
        for ii in range((len(line) - 1) / 3):
            if line[3*ii + 1] == "海湾国家深林公园" or line[3*ii + 1] == "上海海湾国家深林公园":
                tmp_ans["海湾国家森林公园"] = int(line[3*ii + 2])
            elif line[3*ii + 1] == "淮海国际广场":
                tmp_ans["环贸iapm"] = int(line[3*ii + 2])
            elif line[3*ii + 1] == "上海浦东香格里拉大酒店和丽思卡尔大酒店" or line[3*ii + 1] == "上海明捷万丽酒店":
                pass 
            else:
                tmp_ans[line[3*ii + 1]] = int(line[3*ii + 2])
        tmp_ans = tmp_ans.items()
        tmp_ans.sort(key=itemgetter(1))

        if filter:
            try:
                if by == "id":
                    ans.append([ii[0] for ii in tmp_ans if not D_spot_category[ii[0]] in filter])
                    if min_length and len(ans[-1]) < min_length:
                        del ans[-1]
                elif by == "day":
                    tmp_line = dict()
                    for ii in tmp_ans:
                        if not D_spot_category[ii[0]] in filter:
                            try:
                                tmp_line[int(str(ii[1])[:8])].append(ii[0])
                            except KeyError:
                                tmp_line[int(str(ii[1])[:8])] = [ii[0]]
                    if date_range == "all":
                        pass
                    elif type(date_range) == int:
                        if date_range > len(tmp_line.keys()):
                            tmp_line = dict()
                        else:
                            tmp_date_needed = sorted(tmp_line.keys())[date_range-1]
                            tmp_key = tmp_line.keys()
                            for jj in tmp_key:
                                if jj != tmp_date_needed:
                                    tmp_line.pop(jj)
                    else:
                        print "read_route date_range error"
                    for ii in tmp_line.values():
                        if not min_length:
                            ans.append(ii)
                        elif len(ii) >= min_length:
                            ans.append(ii)
                else:
                    print "read route by error"
            except KeyError:
                error_key.append(ii[0])
        else:
            if not min_length:
                ans.append([ii[0] for ii in tmp_ans])
            elif len(tmp_ans) >= min_length:
                ans.append([ii[0] for ii in tmp_ans])
    
    for ii in list(set(error_key)):
        print ii  
    
    return ans
  

def spot_category_read(filename = "spot_category.csv"):
    ans = dict()
    with open(filename, "r") as ff:
        for line in ff:
            ans[line.strip().split(",")[0]] = line.strip().split(",")[1]
    return ans
      
        
if __name__ == "__main__":
    
    ans = read_route()

        
