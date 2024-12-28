#!/bin/bash
rm -f .git/hooks/* .git/hooks/.[!.]* .git/hooks/..?*
cp cleanup.sh .git/hooks/pre-commit
tail -n +2 test.sh >> .git/hooks/pre-commit
