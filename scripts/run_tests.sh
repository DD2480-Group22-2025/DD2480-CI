#!/usr/bin/sh

export CI=true
# should be changed to whatever the path is to the cloned repository
coverage run -m pytest
coverage report
coverage html
cat htmlcov/index.html
