# read days.txt and do some daily statistics with it
# written in python 2.7.13

from datetime import date

f = open("../stats/days.txt")
out = open("../stats/posts_by_date.txt","w")
l = []
for line in f:
    try:
        (d,count) = line.strip().split(' ')
        (year,month,day)=d.strip().split('-')
        postdate = date(int(year),int(month),int(day))
        count = int(count)
    except (ValueError, TypeError):
        continue
    l.append((postdate, count))

l.sort(key=lambda x: x[1], reverse=True)
for day in l:
    print day[0], '\t', day[1]

l.sort(key=lambda x: x[0])
for day in l:
    out.write(str(day[0])+"\t"+str(day[1])+"\n")


f.close()
out.close()
