# read posts_by_date.txt and do some weekly statistics with it
# written in python 2.7.13

from datetime import date, timedelta

f = open("../stats/posts_by_date.txt")
out = open("../stats/posts_by_week.txt","w")
weeks=[]
weeklycount=0
for line in f:
    (d,count)=line.strip().split("\t")
    (year,month,day)=[int(x) for x in d.strip().split("-")]
    d = date(year, month, day)
    weeklycount+=int(count)
    if d.weekday()==6:
        weeks.append((d-timedelta(days=6), d, weeklycount))
        weeklycount=0

weeks.sort(key=lambda x: x[0])
for week in weeks:
    out.write("%s\t%s\t%d\n"%(week[0],week[1],week[2]))

weeks.sort(key=lambda x: x[2], reverse=True)
for week in weeks[:10]:
    print("%s~%s\t%d"%(week[0],week[1],week[2]))

f.close()
out.close()
