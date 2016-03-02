# -*- coding: gb2312 -*-

from operator import itemgetter
import datetime

import freq_route
import route_construct
import sequential_route
import excel_writer
import group_stat


def find_support(itemset, content):
    ans = sum([all((ii in line) for ii in itemset) for line in content]) / float(len(content))
    return ans


def group_gene():
    D_group = dict()
    
    D_id = dict()
    with open("�����Ա��Ϣ��(���lable).txt", "r") as ff:
        for line in ff:
            line = line.strip().split("\t")
            D_id[line[0]] = line[1:]
    
    D_group["region"] = dict()
    for ii in ["��;", "�ж�;", "��;", "�г�;", "��;", "��������"]:
        D_group["region"][ii] = []
    for ii in D_id:
        for jj in ["��;", "�ж�;", "��;", "�г�;", "��;", "��������"]:
            if jj in D_id[ii]:
                D_group["region"][jj].append(ii)
            
    D_group["duration"] = dict()
    for ii in ["1d", "2-3d", "4+d"]:
        D_group["duration"][ii] = []
    for ii in D_id:
        if "ͣ��һ��" in D_id[ii]:
            D_group["duration"]["1d"].append(ii)
        elif "ͣ������" in D_id[ii] or "ͣ������" in D_id[ii]:
            D_group["duration"]["2-3d"].append(ii)
        elif "ͣ������" in D_id[ii] or "ͣ������" in D_id[ii] or "ͣ������" in D_id[ii] \
                or "ͣ������" in D_id[ii] or "��������" in D_id[ii]:
            D_group["duration"]["4+d"].append(ii)
            
    D_group["money"] = dict()
    for ii in ["�е�֧������", "��֧������"]:
        D_group["money"][ii] = []
    for ii in D_id:
        for jj in ["�е�֧������", "��֧������"]:
            if jj in D_id[ii]:
                D_group["money"][jj].append(ii)
                
    D_group["attitude"] = dict()
    for ii in ["�ߴ�����", "����ۻ���", "���������", "���ι�����", "����С����", "��ͥ������"]:
        D_group["attitude"][ii] = []
    for ii in D_id:
        for jj in ["�ߴ�����", "����ۻ���", "���������", "���ι�����", "����С����", "��ͥ������"]:
            if jj in D_id[ii]:
                    D_group["attitude"][jj].append(ii)
                
    D_id_site = dict()
    with open("��ظ��幹���.txt", "r") as ff:
        for line in ff:
            line = line.strip().split("\t")
            D_id_site[line[0]] = line[1:]
            
    D_group["theme"] = dict()
    for ii in ["��ɽɭ�ֹ�԰�ͻ��ֹ�", "������԰", "�Ϻ�����԰", "�Ϻ�Ұ������԰"]:
        D_group["theme"][ii] = []
    for ii in D_id_site:
        for jj in ["��ɽɭ�ֹ�԰�ͻ��ֹ�", "������԰", "�Ϻ�����԰", "�Ϻ�Ұ������԰"]:
            if jj in D_id_site[ii]:
                D_group["theme"][jj].append(ii)   
    
    return D_group


def find_route_main(content, is_include_one = True, min_length=False, min_support=0.008, min_route_support=0.004):
    
    ans = []
    set_ans = []
    route_ans = []
    
    freq_set = freq_route.fpGrowth_main(content, min_support)
    for line in freq_set:
        if len(line) <= 1 and not is_include_one:
            continue
        if len(line) <= min_length and min_length:
            continue
        tmp_ans = sequential_route.sequential_route_construct(content, line, min_route_support)
        set_ans.append(["("+"/".join(line)+")", find_support(line, content)])
        for ii in tmp_ans:
            tmp_line = ["-".join(ii)]
            tmp_line.append(tmp_ans[ii] / float(len(content)))
            route_ans.append(tmp_line)
    route_ans.sort(key=itemgetter(-1), reverse=True)
    set_ans.sort(key=itemgetter(-1), reverse=True)
    
    ans.extend(set_ans)
    ans.extend(route_ans)
    
    return ans


def Main():
    
    ans = dict()
    order_sheet = []
    
    D_group = group_gene()
    
    for filter_set in [["Traffic", "Hotel", "Shopping"], ["Traffic", "Hotel"]]: 
        
        # ���������
        tmp_sheet_name = "nonlocal_all"
        if filter_set == ["Traffic", "Hotel"]:
            tmp_sheet_name += "_withShopping"
        elif filter_set == ["Traffic", "Hotel", "Shopping"]:
            tmp_sheet_name += "_withoutShopping"
        else:
            print "filter_set error"
        content = [ii for ii in route_construct.read_route(filter=filter_set, min_length=3)]
        ans[tmp_sheet_name] = find_route_main(content, min_length=3)
        order_sheet.append(tmp_sheet_name)
        print tmp_sheet_name, "finished"
        
        # ���б�����
        tmp_sheet_name = "local_all"
        if filter_set == ["Traffic", "Hotel"]:
            tmp_sheet_name += "_withShopping"
        elif filter_set == ["Traffic", "Hotel", "Shopping"]:
            tmp_sheet_name += "_withoutShopping"
        else:
            print "filter_set error"
        content = [ii for ii in route_construct.read_route("���ظ��幹���.txt", filter=filter_set)]
        ans[tmp_sheet_name] = find_route_main(content, min_support=0.0001, min_route_support=0.0001)
        order_sheet.append(tmp_sheet_name)
        print tmp_sheet_name, "finished"
        
        
        # ����������ͣ��ʱ����⣩
        for group_standard in D_group:
            for group_name in D_group[group_standard]:
                tmp_sheet_name = group_standard + "_" + group_name
                if filter_set == ["Traffic", "Hotel"]:
                    tmp_sheet_name += "_S"
                elif filter_set == ["Traffic", "Hotel", "Shopping"]:
                    tmp_sheet_name += "_nS"
                else:
                    print "filter_set error"
                content = [ii for ii in route_construct.read_route(
                            id_list=D_group[group_standard][group_name], filter=filter_set, min_length=3)]
                ans[tmp_sheet_name] = find_route_main(content, min_length=3)
                order_sheet.append(tmp_sheet_name)
                print tmp_sheet_name, "finished"
            
        
        # �������ͣ��ʱ��֣�ÿ�������е�����
        for group_standard in ["duration", "region"]:
            for group_name in D_group[group_standard]: 
                for date in ["all", 1, 2, 3, 4, 5, 6, 7]: 
                    tmp_sheet_name = group_standard + "_" + group_name + "_" + str(date)
                    if filter_set == ["Traffic", "Hotel"]:
                        tmp_sheet_name += "_S"
                    elif filter_set == ["Traffic", "Hotel", "Shopping"]:
                        tmp_sheet_name += "_nS"
                    else:
                        print "filter_set error"
                    content = [ii for ii in route_construct.read_route(
                            id_list=D_group[group_standard][group_name], filter=filter_set, by="day", date_range=date)]
                    ans[tmp_sheet_name] = find_route_main(content)
                    order_sheet.append(tmp_sheet_name)
                    print tmp_sheet_name, "finished", len(content)
        
            
    excel_writer.write_excel("disney_route_result", ans, order_sheet=order_sheet)
    return


def sample_Main():
    
    ans = dict()
    order_sheet = []
    
    D_group = group_gene()
    id_info = group_stat.id_info_gene()

    
    tmp_sheet_name = "tmp"
    content = [ii for ii in route_construct.read_route(
                    id_list=D_group["theme"]["�Ϻ�Ұ������԰"], filter=["Traffic", "Hotel", "Shopping"],
                    min_length=3)]
    tmp_ans = find_route_main(content, min_length=3)
    ans[tmp_sheet_name] = group_stat.group_stat_main(
                id_info, tmp_ans, 
                 id_list=D_group["theme"]["�Ϻ�Ұ������԰"], filter=["Traffic", "Hotel", "Shopping"],
                    min_length=3)
    order_sheet.append(tmp_sheet_name)
    
    excel_writer.write_excel("disney_route_result", ans, order_sheet=order_sheet)
    return


if __name__ == "__main__":
    
    start_time = datetime.datetime.now()
    
    Main()

    end_time = datetime.datetime.now()
    print "running time = ", (end_time - start_time).seconds


























