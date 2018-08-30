# nmail
### SMTP mail sender.

With this package you will able to send mails in 1 line.
There is two operations mode:

#### __Config mode__:
   
   Use `config.yml` to specify next variables:
        
        smtp_server: '10.0.0.1'
        smtp_port: 587
        login: 'username@corp.com'
        password: 'password'
   
   Send email with specifying `config.yml` file:
        
        import nmail
        nmail.send_mail(to=['mybro@example.com','someone@example.com'], 
                        cc=['copy@example.com'],
                        bcc=['hidden_copy@example.com'],
                        subject='No subject',
                        text='No Text',
                        attachments=['/tmp/test.txt'],
                        send_as='delegated_mailbox@example.com',
                        config='/tmp/config.yml')
                  
   > If you will not specify __config__ variable - by default nmail will pick config.yml __from package folder__
   
#### __Inline mode__:
   
   Send Email inline:
           
           import nmail
           nmail.send_mail(to=['mybro@example.com','someone@example.com'], 
                           cc=['copy@example.com'],
                           bcc=['hidden_copy@example.com'],
                           subject='No subject',
                           text='No Text',
                           attachments=['/tmp/test.txt'],
                           send_as='delegated_mailbox@example.com',
                           smtp_server='10.0.0.1'
                           smtp_port=587
                           login='username@corp.com'
                           password='password')
                     
   > Also, you may override some of parameters by __specifying__ it in the `send_mail` function call.
   Other params will be gathered from __config file__
   