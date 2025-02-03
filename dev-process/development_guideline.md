## Development Guidelines
Git Guideline
- Branches should be name "../action/description", where action is what is being done (fix,doc,feat,...) and description being a name (or short sentence) which describes what is being done.
- Before starting to work with an issue the team member should make sure to assign him or herself to it so that other team members can see that it is currently being worked on.
- Commits should be atomic (one feature or bug fix), linked to an issue (feat, fix, doc, refactor) and have clear messages with an appropriate prefix.
- Before creating a pull-request the branch must be up-to-date with Main and pass all tests. Before merging a pull-request onto Main it must be approved by AT LEAST one other team member and it must be squished.
- Never rebase a remote branch.

Style Guidelines
- In this project we follow Pythons standard style guides, [PIP 8](https://peps.python.org/pep-0008/) for code style and [PIP 257](https://peps.python.org/pep-0257/) for docstrings.

Testing Guidelines
- Functions should be tested accurately with both positive and negative assertions
- New features should be tested extensively to ensure correctness
