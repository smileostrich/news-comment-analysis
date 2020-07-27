from nrf import db
from nrf.models.models import Comment, News
from nrf.datacollect.forms import DatacollectForm
from sqlalchemy import and_

import requests
import json
from bs4 import BeautifulSoup
import time
import random

oname = {'032': '경향신문', '005': '국민일보', '020': '동아일보', '021': '문화일보', '081': '서울신문', '022': '세계일보', '023': '조선일보', '025': '중앙일보', '028': '한겨레', '469': '한국일보', '421': '뉴스1', '003': '뉴시스', '001': '연합뉴스', '422': '연합뉴스TV', '449': '채널A', '215': '한국경제TV', '437': 'JTBC', '056': 'KBS 뉴스', '214': 'MBC 뉴스', '057': 'MBN', '374': 'SBS CNBC', '055': 'SBS 뉴스', '448': 'TV조선', '052': 'YTN', '009': '매일경제', '008': '머니투데이', '011': '서울경제', '277': '아시아경제', '018': '이데일리', '366': '조선비즈', '123': '조세일보', '014': '파이낸셜뉴스', '015': '한국경제', '016': '헤럴드경제', '079': '노컷뉴스', '119': '데일리안', '417': '머니S', '006': '미디어오늘', '047': '오마이뉴스', '002': '프레시안', '138': '디지털데일리', '029': '디지털타임스', '293': '블로터', '031': '아이뉴스24', '030': '전자신문', '092': 'ZDNet Korea', '045': '로이터', '348': '신화사 연합뉴스', '077': 'AP연합뉴스', '091': 'EPA연합뉴스', '444': '뉴스위크 한국판', '024': '매경이코노미', '308': '시사IN', '586': '시사저널', '262': '신동아', '094': '월간 산', '243': '이코노미스트', '033': '주간경향', '037': '주간동아', '053': '주간조선', '353': '중앙SUNDAY', '036': '한겨레21', '050': '한경비즈니스', '127': '기자협회보', '584': '동아사이언스', '310': '여성신문', '007': '일다', '152': '참세상', '044': '코리아헤럴드', '296': '코메디닷컴', '346': '헬스조선', '087': '강원일보', '088': '매일신문', '082': '부산일보', '298': '정책브리핑', '441': '코리아넷', '468': '스포츠서울', '108': '스타뉴스'}

session = db.session


def initial_request(date, sid1, sid2):
    headers = {
        'User-Agent': 'user-agent 입력',
        'Referer': 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm',
        'charset': 'utf-8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate'
    }
    page = 1

    req = requests.get('http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=' + str(sid1) + '&sid2=' + str(sid2) + '&date=' + str(date) + '&page=' + str(page), headers=headers)
    cont = req.text
    soup = BeautifulSoup(cont, 'html.parser')
    is_next_exist = soup.select('div.paging > a.next')
    if len(is_next_exist) == 1:
        page += 10
        page_count_request(date, sid1, sid2, page)
    elif len(is_next_exist) == 0:
        tot_pagenum = len(soup.select('div.paging > a')) + 1
        get_news_links(date, sid1, sid2, tot_pagenum)


# 뉴스 페이지 수
def page_count_request(date, sid1, sid2, page):
    headers = {
        'User-Agent': 'user-agent 입력',
        'Referer': 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm',
        'charset': 'utf-8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate'
    }
    req = requests.get('http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=' + str(sid1) + '&sid2=' + str(sid2) + '&date=' + str(date) + '&page=' + str(page), headers=headers)
    cont = req.text
    soup = BeautifulSoup(cont, 'html.parser')
    is_next_exist = soup.select('div.paging > a.next')

    if len(is_next_exist) == 1:
        page += 10
        page_count_request(date, sid1, sid2, page)

    elif len(is_next_exist) == 0:
        last_pagenum = soup.select('div.paging > a')
        tot_pagenum = len(last_pagenum) + page - 1
        # print("페이지는 총" + str(tot_pagenum))
        get_news_links(date, sid1, sid2, tot_pagenum)


def get_news_links(date, sid1, sid2, page):
    headers = {
        'User-Agent': 'user-agent 입력',
        'Referer': 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm',
        'charset': 'utf-8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate'
    }

    for i in range(1, page+1):
        req = requests.get('http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=' + str(sid1) + '&sid2=' + str(sid2) + '&date=' + str(date) + '&page=' + str(i), headers=headers)
        cont = req.text
        soup = BeautifulSoup(cont, 'html.parser')
        news_links = soup.select('dl > dt > a')

        for news_link in news_links:
            if news_link.find('img') == None:
                process_news(date, sid1, sid2, news_link['href'])
            else:
                pass


def process_news(date, sid1, sid2, news_link):
    oid = news_link[news_link.find('oid') + 4 : news_link.find('oid') + 7]
    aid = news_link[news_link.find('aid') + 4 : news_link.find('aid') + 14]

    chkExist = News.query.filter(and_(News.aid == str(aid), News.oid == str(oid))).first()

    if chkExist:
        pass
    else:
        headers = {
            'User-Agent': 'user-agent 입력',
            'Referer': 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm',
            'charset': 'utf-8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate'
        }

        req = requests.get(news_link, headers=headers)
        cont = req.text
        soup = BeautifulSoup(cont, 'html.parser')


        # 일부 다른링크로 가버리는 경우, 제목 에러 처리
        if soup.find('h3', {'id': 'articleTitle'}) and soup.find('h3', {'id': 'articleTitle'}).string:
            title_tag = soup.find('h3', {'id': 'articleTitle'})
            title = title_tag.string
            title_replace = title.replace("'", "''")
            date_all = soup.find_all('span', {'class': 't11'})

            news_contents = soup.find_all('div', {'id': 'articleBodyContents'})[0].text
            contents_replace = news_contents.replace("'", "''")
            if oname.get(oid):
                officename = oname.get(oid)
            else:
                officename = ""

            if len(date_all) == 1:
                initial_dt = date_all[0].string
                try:
                    input_data = News(title=title_replace, officename=officename, contents=contents_replace, oid=str(oid), aid=str(aid), sid1=str(sid1), sid2=str(sid2), regtime=initial_dt, simple_dt=date)
                    session.add(input_data)
                    session.commit()
                    session.close()
                except Exception as e:
                    # print('postgresql database connection error!')
                    # print(e)
                    pass
            elif len(date_all) == 2:
                initial_dt = date_all[0].string
                final_dt = date_all[1].string
                try:
                    input_data = News(title=title_replace, officename=officename, contents=contents_replace,
                                      oid=str(oid), aid=str(aid), sid1=str(sid1), sid2=str(sid2), regtime=initial_dt,
                                      modtime=final_dt, simple_dt=date)
                    session.add(input_data)
                    session.commit()
                    session.close()
                except Exception as e:
                    # print('postgresql database connection error!')
                    # print(e)
                    pass

            get_emotion(aid, oid)
            # get_totPage(aid, oid, "")


def get_emotion(aid, oid):
    contentsId = oid + "_" + aid
    news_link = "https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery1124012106969672154722_1531761383659&q=NEWS%5Bne_" + contentsId + "%5D%7CNEWS_MAIN%5Bne_" + contentsId + "%5D"
    req = requests.get(news_link)
    cont = req.content.decode('utf8')
    raw_data = cont[cont.index('({') + 1:-2]
    data = json.loads(raw_data)

    contents_list = data.get('contents')
    like_list = contents_list[0].get('reactions')
    recom_list = contents_list[1].get('reactions')

    like_cnt = int(0)
    warm_cnt = int(0)
    sad_cnt = int(0)
    angry_cnt = int(0)
    want_cnt = int(0)
    recommendmain_cnt = int(0)

    for l_var in like_list:
        l_type = l_var.get('reactionType')
        l_count = l_var.get('count')
        if l_type == "like":
            like_cnt = l_count
        elif l_type == "angry":
            angry_cnt = l_count
        elif l_type == "want":
            want_cnt = l_count
        elif l_type == "warm":
            warm_cnt = l_count
        elif l_type == "sad":
            sad_cnt = l_count

    if recom_list:
        recommendmain_cnt = contents_list[1].get('reactions')[0].get('count')

    data_result = get_totPage(aid, oid, "")
    # 댓글 수
    pdata_count_comment = data_result.get('count').get('comment')  # 대댓글 미포함 (페이징 시 사용)
    pdata_count_reply = data_result.get('count').get('reply')  # 대댓글 수
    pdata_count_total = data_result.get('count').get('total')  # 대댓글 포함 (전체 댓글 수)
    pdata_count_delByUser = data_result.get('count').get('delCommentByUser')  # 유저가 삭제한 댓글 수
    pdata_count_delByMon = data_result.get('count').get('delCommentByMon')  # 규정 미준수
    pdata_count_blindCommentByUser = data_result.get('count').get('blindCommentByUser')
    pdata_count_blindReplyByUser = data_result.get('count').get('blindReplyByUser')
    currentComment_cnt = pdata_count_comment - pdata_count_delByUser - pdata_count_delByMon - pdata_count_blindCommentByUser - pdata_count_blindReplyByUser  # 삭제되지않은 댓글 수

    # 페이지 수
    pdata_page_total = data_result.get('pageModel').get('totalPages')  # 총 페이지
    pdata_page_end = data_result.get('pageModel').get('lastPage')  # 마지막 페이지

    if currentComment_cnt >= 100:
        graph = data_result.get('graph')
        graph_old = graph.get('old')

        # 뉴스 성별 데이터
        man_rate = graph.get('gender').get('male')
        woman_rate = graph.get('gender').get('female')

        # 뉴스 비율 데이터
        teens_rate = graph_old[0].get('value')
        twenties_rate = graph_old[1].get('value')
        thirties_rate = graph_old[2].get('value')
        forties_rate = graph_old[3].get('value')
        fifties_rate = graph_old[4].get('value')

        try:
            # get_emotion
            update_news = News.query.filter(and_(News.aid == str(aid), News.oid == str(oid))).first()
            update_news.like_cnt = int(like_cnt)
            update_news.warm_cnt = int(warm_cnt)
            update_news.sad_cnt = int(sad_cnt)
            update_news.angry_cnt = int(angry_cnt)
            update_news.want_cnt = int(want_cnt)
            update_news.recommendmain_cnt = int(recommendmain_cnt)

            # get_totpage
            update_news.blindreply_cnt = int(pdata_count_blindReplyByUser)
            update_news.blindcomment_cnt = int(pdata_count_blindCommentByUser)
            update_news.violaterule_cnt = int(pdata_count_delByMon)
            update_news.deletedcomment_cnt = int(pdata_count_delByUser)
            update_news.man_rate = int(man_rate)
            update_news.woman_rate = int(woman_rate)
            update_news.teens_rate = int(teens_rate)
            update_news.twenties_rate = int(twenties_rate)
            update_news.thirties_rate = int(thirties_rate)
            update_news.forties_rate = int(forties_rate)
            update_news.fifties_rate = int(fifties_rate)
            update_news.total_cnt = int(pdata_count_total)
            update_news.comment_cnt = int(pdata_count_comment)
            update_news.reply_cnt = int(pdata_count_reply)

            session.merge(update_news)
            session.commit()
            session.close()
        except Exception as e:
            # print('news info data update error')
            # print(e)
            pass
    elif currentComment_cnt < 100:
        try:
            # get_emotion
            update_news = News.query.filter(and_(News.aid == str(aid), News.oid == str(oid))).first()
            update_news.like_cnt = int(like_cnt)
            update_news.warm_cnt = int(warm_cnt)
            update_news.sad_cnt = int(sad_cnt)
            update_news.angry_cnt = int(angry_cnt)
            update_news.want_cnt = int(want_cnt)
            update_news.recommendmain_cnt = int(recommendmain_cnt)

            # get_totpage
            update_news.blindreply_cnt = int(pdata_count_blindReplyByUser)
            update_news.blindcomment_cnt = int(pdata_count_blindCommentByUser)
            update_news.violaterule_cnt = int(pdata_count_delByMon)
            update_news.deletedcomment_cnt = int(pdata_count_delByUser)
            update_news.total_cnt = int(pdata_count_total)
            update_news.comment_cnt = int(pdata_count_comment)
            update_news.reply_cnt = int(pdata_count_reply)

            session.merge(update_news)
            session.commit()
            session.close()
        except Exception as e:
            # print('news info data update error')
            # print(e)
            pass

    parentCommentNo = ""

    if pdata_count_total == 0:
        # print("댓글이 없습니다")
        pass
    else:
        if parentCommentNo:
            process_reply(oid, aid, pdata_page_end, parentCommentNo)
        else:
            process_comment(oid, aid, pdata_page_end)


# 댓글 수와, 뉴스 댓글 비율 데이터(성별, 연령별)
def get_totPage(aid, oid, parentCommentNo):
    headers = {
        'User-Agent': 'user-agent 입력',
        'referer': 'http://news.naver.com/main/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=100&oid=001&aid=0009804092',
        'content-type': 'application/json'
    }
    page = 1
    pCommentNo = '&parentCommentNo=' + parentCommentNo
    req_address = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&pool=cbox5&_callback=jQuery1709954689783071775_1531778938688&lang=ko&objectId=news" + oid + "%2C" + aid + "&pageSize=1000&indexSize=1000&page=" + str(page) + "&initialize=true&userType=&useAltSort=true&replyPageSize=1000&includeAllStatus=true" + pCommentNo
    req = requests.get(req_address, headers=headers)
    cont = req.content.decode('utf8')
    raw_data = cont[cont.index('({') + 1:-2]
    data = json.loads(raw_data)

    data_result = data.get('result')

    return data_result


def process_comment(oid, aid, pdata_page_end):
    headers = {
        'User-Agent': 'user-agent 입력',
        'referer': 'http://news.naver.com/main/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=100&oid=001&aid=0009804092',
        'content-type': 'application/json'
    }
    page = 1

    for i in range(1, int(pdata_page_end) + 1):
        req_address = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&pool=cbox5&_callback=jQuery1709499279192395464_1515568397621&lang=ko&country=&objectId=news" + oid + "%2C" + aid + "&pageSize=1000&indexSize=1000&listType=OBJECT&pageType=more&page=" + str(page) + "&refresh=false&sort=FAVORITE&includeAllStatus=true&_=1515568468166"
        req = requests.get(req_address, headers=headers)
        cont = req.content.decode('utf8')
        raw_data = cont[cont.index('({') + 1:-2]
        data = json.loads(raw_data)
        data_result = data.get('result')

        data_commentlist = data_result.get('commentList')  # db

        for c_data in data_commentlist:
            # commentNo  = 댓글번호 (기본키)
            # replyCount = 대댓글 수
            # replyAllCount = 대댓글 수
            # replyLevel = 대댓글 여부 [1이면 댓글 2면 대댓글]
            # parentCommentNo = 대댓글일 경우 해당 댓글 번호, 댓글일 경우 댓글번호 그대로
            # replyPreviewNo = !미확실 대댓글 번호

            replyAllCount = c_data.get('replyAllCount')
            if replyAllCount != 0:
                parentCommentNo = str(c_data.get('commentNo'))
                get_totPage(aid, oid, parentCommentNo)


            if c_data.get('userIdNo') == None:
                usr_idno = "null"
            else:
                usr_idno = c_data.get('userIdNo')

            cont_replace = c_data.get('contents').replace("'","''")

            try:
                input_data = Comment(useridno=usr_idno, userid=str(c_data.get('userName')), aid=str(aid), oid=str(oid),
                                     contents=cont_replace, commentno=str(c_data.get('commentNo')),
                                     parentcommentno=str(c_data.get('parentCommentNo')),
                                     modtime=c_data.get('modTime'), modtimegmt=c_data.get('modTimeGmt'),
                                     regtime=c_data.get('regTime'), regtimegmt=c_data.get('regTimeGmt'),
                                     blind=bool(c_data.get('blind')),
                                     expose=bool(c_data.get('expose')),
                                     visible=bool(c_data.get('visible')),
                                     secret=bool(c_data.get('secret')),
                                     anonymous=bool(c_data.get('anonymous')),
                                     deleted=bool(c_data.get('deleted')),
                                     blindreport=bool(c_data.get('blindReport')),
                                     best=bool(c_data.get('best')),
                                     mentions=str(c_data.get('mentions')),
                                     sympathycount=int(c_data.get('sympathyCount')),
                                     antipathycount=int(c_data.get('antipathyCount')),
                                     middleblindreport=bool(c_data.get('middleBlindReport')),
                                     replylevel=int(c_data.get('replyLevel')),
                                     replycount=int(c_data.get('replyCount')),
                                     replyallcount=int(c_data.get('replyAllCount')),
                                     idtype=c_data.get('idType'),
                                     idprovider=c_data.get('idProvider')
                                     )
                session.add(input_data)
                session.commit()
                session.close()
            except Exception as e:
                # print('postgresql database connection error!')
                # print(e)
                pass

        page += 1
        # time.sleep(random.randrange(0, 60))


# 대댓글 처리
def process_reply(oid, aid, pdata_page_end, parentCommentNo):
    headers = {
        'User-Agent': 'user-agent 입력',
        'referer': 'http://news.naver.com/main/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=100&oid=001&aid=0009804092',
        'content-type': 'application/json'
    }
    page = 1
    pCommentNo = '&parentCommentNo=' + parentCommentNo

    for i in range(1, int(pdata_page_end) + 1):
        req_address = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&pool=cbox5&_callback=jQuery1709499279192395464_1515568397621&lang=ko&country=&objectId=news" + oid + "%2C" + aid + "&pageSize=1000&indexSize=1000&listType=OBJECT&pageType=more&page=" + str(page) + "&refresh=false&sort=FAVORITE&includeAllStatus=true&_=1515568468166" + pCommentNo
        req = requests.get(req_address, headers=headers)
        cont = req.content.decode('utf8')
        raw_data = cont[cont.index('({') + 1:-2]
        data = json.loads(raw_data)
        data_result = data.get('result')

        data_commentlist = data_result.get('commentList')  # db

        for c_data in data_commentlist:

            if c_data.get('userIdNo') == None:
                usr_idno = "null"
            else:
                usr_idno = c_data.get('userIdNo')

            cont_replace = c_data.get('contents').replace("'", "''")

            try:
                input_data = Comment(useridno=usr_idno, userid=str(c_data.get('userName')), aid=str(aid), oid=str(oid),
                                     contents=cont_replace, commentno=str(c_data.get('commentNo')),
                                     parentcommentno=str(c_data.get('parentCommentNo')),
                                     modtime=c_data.get('modTime'), modtimegmt=c_data.get('modTimeGmt'),
                                     regtime=c_data.get('regTime'), regtimegmt=c_data.get('regTimeGmt'),
                                     blind=bool(c_data.get('blind')),
                                     expose=bool(c_data.get('expose')),
                                     visible=bool(c_data.get('visible')),
                                     secret=bool(c_data.get('secret')),
                                     anonymous=bool(c_data.get('anonymous')),
                                     deleted=bool(c_data.get('deleted')),
                                     blindreport=bool(c_data.get('blindReport')),
                                     best=bool(c_data.get('best')),
                                     mentions=str(c_data.get('mentions')),
                                     sympathycount=int(c_data.get('sympathyCount')),
                                     antipathycount=int(c_data.get('antipathyCount')),
                                     middleblindreport=bool(c_data.get('middleBlindReport')),
                                     replylevel=int(c_data.get('replyLevel')),
                                     replycount=int(c_data.get('replyCount')),
                                     replyallcount=int(c_data.get('replyAllCount')),
                                     idtype=c_data.get('idType'),
                                     idprovider=c_data.get('idProvider')
                                     )
                session.add(input_data)
                session.commit()
                session.close()
            except Exception as e:
                # print('postgresql database connection error!')
                # print(e)
                pass

        page += 1
        # time.sleep(random.randrange(0, 60))
