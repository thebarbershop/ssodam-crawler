#-*- coding: utf-8 -*-
# read comments.txt, likes.txt, or views.txt and make some html tags
# written in python 2.7.13

# configuration
max_print = 10  # max number of elements to print
content_url_base = "http://www.ssodam.com/content/"  # content url without post number


def main():
    # open a different file to print by likes or comments
    f = open('../stats/views.txt')
    c = 0
    for line in f:
        if c > max_print:
            break
        (postid, title, comments, likes, postdate, views) = line.strip().split("\t")
        content_url = content_url_base + postid
        (year,month,day) = postdate.strip().split("-")

        # change this print line ("조회수" and views) to print by likes or comments
        print "<a href =""%s"">%s</a> (조회수 %s개, %s년 %s월 %s일)<br>" % (content_url, title, views, year, month, day)
        c += 1
    f.close()

if __name__ == "__main__":
    main()
