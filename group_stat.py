# -*- coding: cp936 -*-


from operator import itemgetter


def spot_category_read(filename = "spot_category.csv"):
    ans = dict()
    with open(filename, "r") as ff:
        for line in ff:
            ans[line.strip().split(",")[0]] = line.strip().split(",")[1]
    return ans


def route_extract(route, spot_set, is_sequential=False):
    tmp = [route[ii] for ii in xrange(len(route)) 
                if (not route[ii] in route[:ii]) and route[ii] in spot_set]
    if is_sequential:
        ans = (tuple(tmp) == tuple(spot_set))
    else:
        ans = (len(tmp) == len(spot_set))
    return ans


def find_id_set_from_route(L_spot_set, filename="外地个体构造表.txt", 
                is_sequential=False, filter=None, min_length=False, id_list=False,
                 by="id", date_range="all"):
    
    ans = dict()
    
    with open(filename, "r") as ff:
        content = [line.strip().split("\t") for line in ff]
    
    D_spot_category = spot_category_read(filename = "spot_category.csv")    
    
    for ii in D_spot_category:
        print ii,
    print
    
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
                    tmp_route = [ii[0] for ii in tmp_ans if not D_spot_category[ii[0]] in filter]
                    if min_length and len(tmp_route) < min_length:
                        continue
                    else:
                        for spot_set in L_spot_set:
                            if route_extract(tmp_route,
                                        spot_set=spot_set, is_sequential=is_sequential):
                                ans[tuple(spot_set)].append(line[0])
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
                    for tmp_route in tmp_line.values():
                        if not min_length:
                            for spot_set in L_spot_set:
                                if route_extract(tmp_route,
                                            spot_set=spot_set, is_sequential=is_sequential):
                                    ans[tuple(spot_set)].append(line[0])
                        elif len(ii) >= min_length:
                            for spot_set in L_spot_set:
                                if route_extract(tmp_route,
                                            spot_set=spot_set, is_sequential=is_sequential):
                                    ans[tuple(spot_set)].append(line[0])
                else:
                    print "read route by error"
            except KeyError:
                error_key.append(ii[0])
        else:
            if not min_length:
                for spot_set in L_spot_set:
                    if route_extract([ii[0] for ii in tmp_ans],
                                        spot_set=spot_set, is_sequential=is_sequential):
                        ans[tuple(spot_set)].append(line[0])
            elif len(tmp_ans) >= min_length:
                for spot_set in L_spot_set:
                    if route_extract([ii[0] for ii in tmp_ans],
                                        spot_set=spot_set, is_sequential=is_sequential):
                        ans[tuple(spot_set)].append(line[0])
    
    print "error key:"
    for ii in list(set(error_key)):
        if ii in D_spot_category:
            print ii
        else:
            print "other", ii  
    print "***************"
    
    for ii in ans:
        ans[ii] = list(set(ans[ii]))
        for jj in ii:
            print jj,
        print 
    
    return ans


def id_info_gene():
    ans = dict()
    
    D_id = dict()
    with open("外地人员信息表(打过lable).txt", "r") as ff:
        for line in ff:
            line = line.strip().split("\t")
            D_id[line[0]] = line[1:]
            
    for idd in D_id:
        ans[idd] = dict()
        
        ans[idd]["duration"] = None
        for jj, ii in enumerate(["停留一天", "停留两天", "停留三天", "停留四天", 
                                 "停留五天", "停留六天", "停留七天","七天以上"]):
            if ii in D_id[idd]:
                ans[idd]["duration"] = jj + 1
                
        ans[idd]["region"] = None
        for ii in ["短途", "中短途", "中途", "中长途", "长途", "北京地区"]:
            if ii in D_id[idd]:
                ans[idd]["region"] = ii
                
        ans[idd]["money"] = None
        for ii in ["中等支付能力", "高支付能力"]:
            if ii in D_id[idd]:
                ans[idd]["money"] = ii
                
        ans[idd]["attitude"] = None
        for ii in ["高大上型", "走马观花型", "深度游玩型", "旅游购物型", "文艺小资型", "家庭亲子型"]:
            if ii in D_id[idd]:
                ans[idd]["attitude"] = ii
        
        ans[idd]["get_off_time"] = float(D_id[idd][7]) if D_id[idd][7] != "NULL" and D_id[idd][7] != "Unknown" else None
        ans[idd]["end_time"] = float(D_id[idd][8]) if D_id[idd][8] != "NULL" and D_id[idd][8] != "Unknown" else None
        ans[idd]["traffic_arrive"] = D_id[idd][2]
        ans[idd]["traffic_departure"] = D_id[idd][3]
        ans[idd]["province"] = D_id[idd][4]
        
    return ans


def find_mode(L_content):
    if len(L_content) == 0:
        return "NA"
    tmp = dict()
    for ii in L_content:
        tmp[ii] = tmp.get(ii, 0) + 1
    tmp = tmp.items()
    tmp.sort(key=itemgetter(1), reverse=True)
    return tmp[0][0]


def find_mean(L_num):
    try:
        tmp = [float(ii) for ii in L_num if ii]
        return sum(tmp) / len(tmp)
    except ZeroDivisionError:
        return "NA"


def group_stat(id_info, L_id):
    get_off_time = find_mean([id_info[ii]["get_off_time"] for ii in L_id])
    end_time = find_mean([id_info[ii]["end_time"] for ii in L_id])
    traffic = find_mode([id_info[ii]["traffic"] for ii in L_id])
    province = find_mode([id_info[ii]["province"] for ii in L_id])
    stay_mode = find_mode([id_info[ii]["duration"] for ii in L_id])
    stay_mean = find_mean([id_info[ii]["duration"] for ii in L_id])
    ans = [len(L_id), get_off_time, end_time, traffic, province, stay_mode, stay_mean]
    return ans


def group_stat_main(id_info, L_spot_set_ans, filename="外地个体构造表.txt", 
                 filter=None, min_length=False, id_list=False,
                 by="id", date_range="all"):
    ans = []
    L_spot_set = []
    L_route_set = []
    for line in L_spot_set_ans:
        tmp = line[0]
        if "(" in tmp:
            L_spot_set.append(tmp[1:(len(tmp)-1)].split("/"))
        else:
            L_route_set.append(tmp.split("-"))

    L_id_set = find_id_set_from_route(L_spot_set, filename=filename, 
                    is_sequential=False, filter=filter, min_length=min_length,
                     id_list=id_list,
                     by=by, date_range=date_range)
    L_id_route = find_id_set_from_route(L_spot_set, filename=filename, 
                    is_sequential=True, filter=filter, min_length=min_length,
                     id_list=id_list,
                     by=by, date_range=date_range)
    
    for ii in L_id_set:
        for jj in ii:
            print jj,
        print len(L_id_set[ii])
    for ii in L_id_route:
        for jj in ii:
            print jj,
        print len(L_id_route[ii])

    for line in L_spot_set_ans:
        tmp_ans = [line[0], line[1]]
        tmp = line[0]
        if "(" in tmp:
            try:
                tmp_group_stat = group_stat(id_info, L_id_set[tuple(tmp[1:(len(tmp)-1)].split("/"))])
            except KeyError:
                for ii in tuple(tmp[1:(len(tmp)-1).split("/")]):
                    print ii,
                print           
        else:
            tmp_group_stat = group_stat(id_info, L_id_route[tuple(tmp.split("-"))])
        tmp_ans.extend(tmp_group_stat)
        ans.append(tmp_ans)
    return ans


if __name__ == "__main__":
    spot_category_read()






















