#!/usr/bin/env  python
# -*-coding: utf-8-*-

'''
http://exercise.acmcoder.com/online/online_judge_ques?ques_id=4398&konwledgeId=41
公司最近新研发了一种产品，共生产了n件。有m个客户想购买此产品，第i个客户出价Vi元。
为了确保公平，公司决定要以一个固定的价格出售产品。
每一个出价不低于要价的客户将会得到产品，余下的将会被拒绝购买。请你找出能让公司利润最大化的售价。
样例输入
    5 4

    2 8 10 7
样例输出
7
'''

m,n = map(int, raw_input().split(' '))
vi = [ x for x in map(int, raw_input().split(' '))]
vi.sort()
price, money = 0, 0
for i in range(n):
    if money < vi[i] * min((n - i), m):
        price, money = vi[i], vi[i] * min((n - i), m)
print price
