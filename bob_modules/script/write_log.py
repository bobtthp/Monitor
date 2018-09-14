import time

while True:
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    with open('tmpfile/test.log', 'a') as f:
        f.write(now + 'it is a test' + '\n')
        time.sleep(2)
        print now
