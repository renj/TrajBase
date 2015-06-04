page_num = 1
i = 0
head = 'GPSID,X,Y,TIME,SPEED,DIR\r\n'
page = head
file_start = '/home/renj/Data/zhengjiang_'
total = 155734962
idx = 0

date = '01'
with open('/home/renj/Data/09.sql', 'r') as fp:
    for s in fp:
        idx += 1
        if i % 100000 == 9999:
            print i
        if s.startswith('values'):
            #print s
            line = s[8:-4].replace("'", '').replace('to_date(', '').replace("dd-mm-yyyy hh24:mi:ss), ", '')+'\r\n'
            #page += s
            #print date, line.split(',')[3].strip()[:2]
            if line.find('dd') != -1:
                continue
            today = line.split(',')[3].strip()[:2]
            if date != today:
                print date, today
                file_name = file_start+str(page_num)+'.txt'
                print file_name
                with open(file_name, 'w') as _f:
                    _f.write(page)
                page = head
                i = 0
                page_num += 1
                date = today
            page += line
            i += 1
'''

for i in range(38):
    file_name = file_start+str(i)+'.txt'
    print file_name
    with open(file_name, 'r') as fp:
        page = head
        for s in fp:
            if s.find('-2014,'):
                print i
                break
'''