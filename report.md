# Report

## Summary of compilation and testing
This CI server supports compiling and running a syntax check on the project. It is triggered as a webhook whenever there is a push to this project. The compilation feature is unit-tested in `/tests/test_syntax.py`. 

## Test execution and implementation
This CI server supports executing the automated tests of our group project. It is triggered with the webhook on the specific branch and executes the unit tests. It is also unit tested in `/tests/test_runner.py`

## Notification implementation
There are notifications for the CI results. The commit status is set for the repository after the above checks and tests are triggered. It is unit tested in `/tests/test_notifier.py`

## Statement of Contributions

[ Carl ]
- CI feature: database and history of past builds
- writing the report and "way of working"
- update README 

[ Jacob ]
- core CI feature for #2 testing
- testing the database

[ Klara ]
- core CI feature #3 for notifications
- testing for notifications

[ Phoebe ]
- core CI feature #1 for compiling and syntax checking
- testing for compiling and syntax checking

[ Samuel ]
- setup server
- testing for the CI testing feature
- database handling and testing

## Way of working 
Referring to Table 8.6 in the Essence standard v1.2, our team is currently in the [ Formed ] state, progressing towards the [ Collaborating ] state. Individual responsibilities are understood, and each team member is doing it's best to finish their task in the best way possible according to their individual competencies. Furthermore, every team member understands their role in the group and how to perform their work. If any team member experiences problems with their assignments, the member asks the others in the group for help. The work is being conducted both during individual sessions and group meetings with Discord as the primary platform for communication.

