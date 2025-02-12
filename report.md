# Report

## Summary of compilation and testing
This CI server supports compiling and running a syntax check on the project. It is triggered as a webhook whenever there is a push to this project. The compilation feature is unit-tested in `/tests/test_syntax.py`. 

## Test execution and implementation
This CI server supports executing the automated tests of our group project. It is triggered with the webhook on the specific branch and executes the unit tests. It is also unit tested in `/tests/test_runner.py`

## Notification implementation
There are notifications for the CI results. The commit status is set for the repository after the above checks and tests are triggered. It is unit tested in `/tests/test_notifier.py`

## Development Guidelines
Git Guideline
- Branches should be named "../action/description", where action is what is being done (fix, doc, feat, ...) and description being a name (or a short underscore separated sentence) which describes what is being done.
- Before starting to work on an issue the team member should make sure to assign him or herself to it so that other team members can see that it is currently being worked on.
- Commits should be atomic (one feature or bug fix), linked to an issue (feat, fix, doc, refactor) and have clear messages with an appropriate prefix.
- Before creating a pull-request the branch must be up-to-date with Main and pass all tests. Before merging a pull-request onto Main it must be approved by AT LEAST one other team member, and it must be squashed.
- Never rebase a remote branch.

Style Guidelines
- In this project we follow Pythons standard style guides, [PIP 8](https://peps.python.org/pep-0008/) for code style and [PIP 257](https://peps.python.org/pep-0257/) for docstrings.

Testing Guidelines
- Functions should be tested accurately with both positive and negative assertions
- New features should be tested extensively to ensure correctness

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

