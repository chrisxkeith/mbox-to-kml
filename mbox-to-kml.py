import mailbox
import time
import base64
import re

class mboxToKml:
    def run(self):
        start = time.time()
        mbox = mailbox.mbox(r'2020-10-emails.mbox')
        converted = 0
        for i, message in enumerate(mbox):
            if i == 0:
                end = time.time()
                print('Open mbox file: ' + str(end - start) + ' seconds')
            if message['from'] == 'Christopher Keith <chris.keith@gmail.com>':
                if message.is_multipart():
                    for part in message.get_payload():
                        if part._default_type == 'text/plain':
                            thePart = part.as_string()
                            if isinstance(thePart,str):
                                theStr = thePart
                            else:
                                theStr = thePart.as_string()
                            if 'image/png' in theStr:
                                self.convert_to_png(message['subject'], thePart)
                        else:
                            print('Message# : ' + str(i) + ': unhandled: ' + part._default_type)
                else:
                    print('Message# : ' + str(i) + ': not multipart')
                converted = converted + 1
        end = time.time()
        print('Total run time: ' + str(end - start) + ' seconds')
        print('converted: ' + str(converted))

    def convert_to_png(self, subject, thePart):
        subject = subject.replace(' ', 'xxxxx')
        subject = re.sub(r'Re: ', '', subject)
        subject = re.sub(r'Seen on a past walk', '', subject)
        fname = re.sub(r'\W', '', subject) + '.png'
        fname = fname.replace('xxxxx', ' ')
        fname = fname.replace('Seen on todays walk ', '')
        pastHeaders = False
        pngData = ''
        for aLine in thePart.split('\n'):
            if pastHeaders:
                pngData = pngData + (aLine + '\n')
            if aLine == '':
                pastHeaders = True
        g = open(fname, "w")
        g.write(str(base64.b64decode(pngData)))
 
mboxToKml().run()
