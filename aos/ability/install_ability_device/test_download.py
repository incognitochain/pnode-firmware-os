import urllib2

import sys

link = 'http://s3-autonomous.s3.amazonaws.com/personal_assistant.zip'
zip_file = 'personal_assistant.zip'
try:

    print 'Downloading app >> ...', link
    print 'Save to %s...' % zip_file
    request = urllib2.urlopen(link, timeout=10)
    file_size = int(request.info().getheaders("Content-Length")[0])


    size = 0
    block_sz = 131072

    zip_file = open(zip_file, 'wb')

    while True:
        buffer = request.read(block_sz)
        if not buffer:
            break
        size += len(buffer)
        percentage = float(float(size) / float(file_size)) * 100

        zip_file.write(buffer)

        print "Downloaded: " + ("%.2f" % percentage) + " %", percentage

    zip_file.close()

    print "Finished!".ljust(20, ' ')


except urllib2.HTTPError as e:
    print "HTTP Error:", e.code, link
except urllib2.URLError as e:
    print "URL Error:", e.reason, link
except Exception as e:
    print str(e)
    print "error update ....", sys.exc_info()