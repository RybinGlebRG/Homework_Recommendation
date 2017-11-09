import csv
import math


k=5
user=27

def similar(u,v):
    return similarity[u][v]

def r(v,i):
    return data[v][i]

def r_av(v):
    return average[v]

def r_c(v,i):
    return context[v][i]


def getData():
    data = [0]
    with open("data.csv", "r", newline="") as file:
        read = csv.reader(file)
        i = 0
        for row in read:
            if row[0] != '':
                data[i] = [0] * (len(row) - 1)
                j = 0
                for el in row[1:]:
                    data[i][j] = int(el)
                    j += 1
                i += 1
                data.append(0)
        data.pop()
    return data

def calcAverage(data):
    average=[]
    for row in data:
        sum = 0
        count = 0
        for el in row:
            if el != -1:
                sum += el
                count += 1
        average.append(sum / count)
    return  average

def calcSimilarity(data,user):

    similarity=[0]*len(data)
    for i in range(0,len(similarity)):
        if i==user:
            similarity[i]=-1
        else:
            sim = 0
            usqrt = 0
            vsqrt = 0
            for j in range(0,len(data[user])):
                if data[user][j]!=-1 and data[i][j]!=-1:
                    sim+=data[user][j]*data[i][j]
                    usqrt+=data[user][j]**2
                    vsqrt+=data[i][j]**2
            similarity[i]=round(sim/((usqrt**(1/2))*(vsqrt**(1/2))),3)
    return similarity


def findNearest(similarity):

    lst=sorted(similarity)
    max5=[]
    for i in range(0,5):
        max = 0
        for i in range(0,len(similarity)):
            if similarity[i]>similarity[max] and i not in max5:
                max=i
        max5.append(max)
    return max5


def calcEmpty(user,nearest,similarity,average):
    res=getData()
    for i in range(0,len(res[user])):
        if res[user][i]==-1:
            numerator = 0
            denominator = 0
            for j in nearest:
                if res[j][i]!=-1:
                    sim=similarity[j]
                    vr=res[j][i]
                    vra=average[j]
                    numerator+=sim*(vr-vra)
                    denominator+=math.fabs(sim)
            res[user][i]=round(average[user]+numerator/denominator,2)
    return res


def show(lst):
    for row in lst:
        print(row)

def assResult(data,result,context,result_c,user):
    res = {}
    res_c = {}
    headers=[]
    headers_c = []
    with open("data.csv", "r", newline="") as file:
        read = csv.reader(file)
        for row in read:
            if row[0] == '':
                for el in row[1:]:
                    headers.append(el)

    with open("context.csv", "r", newline="") as file:
        read = csv.reader(file)
        for row in read:
            if row[0] == '':
                for el in row[1:]:
                    headers_c.append(el)

    for i in range(0,len(data[user])):
        if data[user][i]==-1:
            res[headers[i][1:].lower()]=result[user][i]
    h_lst=[]
    for i in range(0, len(context[user])):
        if context[user][i]==-1 and result_c[user][i] > 0 and result_c[user][i] < 6  :
            res_c[headers_c[i]] = result_c[user][i]
            h_lst.append(headers_c[i])

    max=res_c[h_lst[0]]
    cur=0
    for i in range(1,len(res_c)):
        if res_c[h_lst[i]]<=max:
            res_c.pop(h_lst[i])
        else:
            res_c.pop(h_lst[cur])
            cur=i
            max=res_c[h_lst[cur]]

    payload = {"user": user + 1, "1": res, "2": res_c}
    return payload

def getContext():
    context = [0]
    with open("context.csv", "r", newline="") as file:
        read = csv.reader(file)
        i = 0
        for row in read:
            if row[0] != '':
                context[i] = [0] * (len(row) - 1)
                j = 0
                for el in row[1:]:
                    if el == " Mon":
                        context[i][j] = 1
                    elif el == " Tue":
                        context[i][j] = 2
                    elif el == " Wed":
                        context[i][j] = 3
                    elif el == " Thu":
                        context[i][j] = 4
                    elif el == " Fri":
                        context[i][j] = 5
                    elif el == " Sat":
                        context[i][j] = 6
                    elif el == " Sun":
                        context[i][j] = 7
                    else:
                        context[i][j] = -1
                    j += 1
                i += 1
                context.append(0)
        context.pop()
    return context

def calcEmpty_c(nearest,user,similarity):
    res=getContext()
    aver=0
    count=0
    for i in range(0,len(res[user])):
        if res[user][i]!=-1:
            aver+=res[user][i]
            count+=1
    aver/=count

    for i in range(0,len(res[user])):
        if res[user][i]==-1:
            numerator=0
            denominator=0
            for j in nearest:
                sim=similarity[j]
                vr=res[j][i]
                vra=aver
                numerator+=sim*(vr-vra)
                denominator+=math.fabs(sim)
            tmp=aver+numerator/denominator
            res[user][i]=tmp
    return  res

'''
def findPayload(str):
    for i in range(100, 501):
        payload = {'user': 28, '1': {'movie 1': i/100, 'movie 2': 3.99, 'movie 9': 2.45, 'movie 11': 2.33}, '2': {}}
    #print(payload)
        response = rq.post("https://cit-home1.herokuapp.com/api/rs_homework_1", json=payload)
    ##print(response.content)
        if response.content != str:
            return i/100
'''



data=getData()

average=calcAverage(data)

similarity=calcSimilarity(data,user)

nearest=findNearest(similarity)

result=calcEmpty(user,nearest,similarity,average)

context=getContext()

result_c=calcEmpty_c(nearest,user,similarity)
payload=assResult(data,result,context,result_c,user)
print(payload)

import requests as rq

response = rq.post("https://cit-home1.herokuapp.com/api/rs_homework_1", json=payload)
print(response.content)


