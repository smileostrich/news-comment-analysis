from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


def main():
    # sday = datetime(2017, 5, 1)
    # eday = datetime(2017, 12, 31)
    # # test = datetime(20180101)
    #
    # test2 = '20180101'
    conver_date = datetime.strptime(test2, '%Y%m%d').date()
    # # print(type(conver_date))
    # # test4 = datetime(conver_date)
    # # print(test4)
    # ttt = (conver_date - sday).days
    # print(ttt)
    # print(sday)

    # totday = (eday - sday).days
    # v_day = 0
    # for test in range(0, totday+1):
    #     # test1 = sday
    #     test1 = sday + timedelta(days=test)
    #     test2 = sday + timedelta(days=test+1)
    #     print(test1, test2)
    #     v_day += 1
    #
    # print(v_day)
    # print(totday)
    # test = default_time + timedelta(days=1)

    # print(test2)
    # print(test3)
    # print(test4)

    # sday = datetime(2017, 5, 1).date()
    # eday = datetime(2017, 12, 31).date()
    # print((eday - sday).days)



main()
