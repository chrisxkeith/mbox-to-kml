import mailbox
import time
import base64

class mboxToKml:
    def run(self):
        start = time.time()
        mbox = mailbox.mbox(r'2020-10-emails.mbox')
        converted = 0
        for i, message in enumerate(mbox):
            if i == 0:
                end = time.time()
                print('Open file: ' + str(end - start) + ' seconds')
            if message['from'] == 'Christopher Keith <chris.keith@gmail.com>':
                converted = converted + 1
                if message.is_multipart():
                    for part in message.get_payload():
                        if part._default_type == 'text/plain':
                            thePart = part.as_string()
                            if 'image/png' in thePart.as_string():
                                cvtMessage = self.convert_to_png(thePart)
                        else:
                            print('Message# : ' + str(i) + ': unhandled: ' + part._default_type)
                else:
                    print('Message# : ' + str(i) + ': not multipart')
                print('subj: ' + message['subject'])
                print('date: ' + message['date'])
                print('conv: ' + cvtMessage)
        end = time.time()
        print('Total run time: ' + str(end - start) + ' seconds')
        print('converted: ' + str(converted))

    def convert_to_png(self, thePart):
        return 'stub'
        # g = open(fname, "w")
        # g.write(base64.decodestring(base64str))
 
mboxToKml().run()
