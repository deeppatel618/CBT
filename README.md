
# CBT

COMPUTER BASED TEST Web Application helps to conduct Multiple choice question exam .

This application is primarily for two types of users: students and faculty.
Faculty have the authority to create various tests based on various courses.Students can take the exam and receive the results through email.

## Features

- Maintaining Sessions of different users
- Managing Profile
- Sending Email
- Sending SMS
- AJAX

`django.core.mail` module is used to send Email to users.

For sending SMS `Twilio` API is used.

`AJAX` is used to approve Student status by Faculty. 
