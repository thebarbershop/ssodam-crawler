# ssodam crawler for educational, statistic and entertainment purposes
# written in python 2.7.13

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

# configuration
max_elements = 100  # max number of elements to print for each category
timedifference = 8 * 60  # (ssodam time zone = GMT+9) - (crawler time zone = GMT+1) in minutes
# first_page = 560  # delete this line to crawl from the beginning of the board
# last_page = 565  # delete this line to crawl until the end of the board
main_url = "http://www.ssodam.com/"
login_url = "http://www.ssodam.com/auth"
board_url_base = "http://www.ssodam.com/board/5/"  # board url without page number
content_url_base = "http://www.ssodam.com/content/"  # content url without post number


class Post:
    def __init__(self, feed, title="", comments=0, likes=0, postdate=date(1, 1, 1), views=0):
        if isinstance(feed, str):
            (postid, title, comments, likes, postdate, views) = feed.strip().split("\t")
            (year, month, day) = postdate.split("-")
            postdate = date(int(year), int(month), int(day))
        else:
            postid = feed if isinstance(feed, int) else 0

        self.postid = int(postid)
        self.title = title
        self.comments = int(comments)
        self.likes = int(likes)
        self.postdate = postdate
        self.views = int(views)

    def __str__(self):
        try:
            return "%d\t%s\t%d\t%d\t%s\t%d" % (
                self.postid, self.title.encode('utf8'), self.comments,
                self.likes, self.postdate, self.views)
        except UnicodeDecodeError:
            return "%d\t%s\t%d\t%d\t%s\t%d" % (
                self.postid, self.title, self.comments,
                self.likes, self.postdate, self.views)


def crawl():
    session = requests.session()

    # login
    print "Login Attempt"
    username, password = raw_input("\tid: "), raw_input("\tpassword: ")
    csrftoken = session.get(main_url).cookies["csrftoken"]
    payload = {
        "id": username,
        "password": password,
        "auto": "false",
        "csrfmiddlewaretoken": csrftoken
    }
    result = session.post(login_url, data=payload, headers={"Referer": main_url})
    if result.status_code != 200:
        print "Login Failure"
        return
    else:
        print "Login Success"

    # get first_ and last_page
    result = session.get(board_url_base + "1")
    soup = BeautifulSoup(result.text, "lxml")
    if "first_page" not in globals():
        first_page = 1
    if "last_page" not in globals():
        last_page = int(soup.text[soup.text.find("max_page"):].split('\n')[0][0:-1].split(" ")[1])

    # figure out announcements
    announcements = set()  # contains post number of announcements
    for label in soup.find_all("span", "label label-info"):
        announcements.add(int(label.find_next_sibling("a")['href'].split('/')[2].split('?')[0]))

    year = (datetime.now() + timedelta(minutes=timedifference)).year

    # crawl each page and collect data
    f_posts = open("data/posts.txt", "w")
    posts = []
    print "Crawl Start"
    for page in range(first_page, last_page + 1):
        board_url = board_url_base + str(page)
        result = session.get(board_url)
        soup = BeautifulSoup(result.text, "lxml")
        for td in soup.find_all("td", "mobile-hide"):
            try:
                if int(td.text) in announcements:
                    continue
            except ValueError:
                continue
            postid = int(td.text)
            td = td.find_next("td", "title title-align")
            if td.find("a", href="alert();") is not None:
                continue  # Frozen post
            title = td.find("a").text.strip()
            try:
                comments = int(td.find("span", "comment-num").text.strip("[]"))
            except (AttributeError, ValueError):  # post with no comments
                comments = 0
            td = td.find_next("td").find_next("td")
            likes = int(td.text.strip())
            td = td.find_next("td")
            try:
                month, day = [int(x) for x in td.text.strip().split('/')]
                if (month, day) == (12, 31) and posts[-1].postdate.month == 1:
                    year -= 1
            except (ValueError, IndexError):
                continue  # too recent post, not 24 hours old yet
            postdate = date(year, month, day)
            td = td.find_next("td")
            views = int(td.text.strip())
            posts.append(Post(postid, title, comments, likes, postdate, views))
            f_posts.write(str(posts[-1]) + "\n")
        print "\tReading page %d of %d (%.2f%%)" % (
            page, last_page, 100.0 * (page - first_page + 1) / (last_page - first_page + 1))

    print "Crawl Done"
    f_posts.close()
    session.close()
    return posts


def readposts():
    print "Read Posts Start"
    f_posts = open("data/posts.txt")
    posts = []
    for line in f_posts:
        posts.append(Post(line))
    f_posts.close()
    print "Read Posts Done"
    return posts


def statistics(posts):
    global max_elements
    max_elements = min(max_elements, len(posts))

    print "Statistic Processing Start"
    print "\tComments"
    f_comments = open("stats/comments.txt", "w")
    most_comments = posts[:max_elements]
    most_comments.sort(key=lambda p: p.comments, reverse=True)
    for post in posts[max_elements:]:
        if post.likes > most_comments[-1].comments:
            most_comments[-1] = post
            most_comments.sort(key=lambda p: p.comments, reverse=True)
    for post in most_comments:
        f_comments.write(str(post) + "\n")
    f_comments.close()

    print "\tLikes"
    f_likes = open("stats/likes.txt", "w")
    most_likes = posts[:max_elements]
    most_likes.sort(key=lambda p: p.likes, reverse=True)
    for post in posts[max_elements:]:
        if post.likes > most_likes[-1].likes:
            most_likes[-1] = post
            most_likes.sort(key=lambda p: p.likes, reverse=True)
    for post in most_likes:
        f_likes.write(str(post) + "\n")
    f_likes.close()

    print "\tViews"
    f_views = open("stats/views.txt", "w")
    most_views = posts[:max_elements]
    most_views.sort(key=lambda p: p.views, reverse=True)
    for post in posts[max_elements:]:
        if post.views > most_views[-1].views:
            most_views[-1] = post
            most_views.sort(key=lambda p: p.views, reverse=True)
    for post in most_views:
        f_views.write(str(post) + "\n")
    f_views.close()

    print "\tDays"
    f_days = open("stats/days.txt", "w")
    count_by_weekday = {}
    count_by_date = {}
    for i in range(0, 7):
        count_by_weekday[i] = 0
    for post in posts:
        try:
            count_by_date[post.postdate] += 1
        except KeyError:
            count_by_date[post.postdate] = 1
        count_by_weekday[post.postdate.weekday()] += 1
    for weekday in count_by_weekday:
        f_days.write(
            "%s %d\n" % (["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][weekday], count_by_weekday[weekday]))
    f_days.write("\n")
    for postdate in count_by_date:
        f_days.write("%s %d\n" % (postdate, count_by_date[postdate]))
    f_days.close()

    print "Statistic Done"


def main():
    posts = crawl()
    if posts is None:
        return
    statistics(posts)


if __name__ == "__main__":
    main()
