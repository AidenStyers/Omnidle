#!/bin/bash
set -e

echo "VITAL: Make sure all of your local changes are committed! Otherwise only some of the commands will run. CTRL-C right now and check!!"

read -p "Enter the name of the branch to un-archive: " BRANCH_NAME

git checkout -b $BRANCH_NAME archive/$BRANCH_NAME
git push origin $BRANCH_NAME --no-verify
git tag -d archive/$BRANCH_NAME
git push origin --delete archive/$BRANCH_NAME --no-verify

echo "$BRANCH_NAME un-archived!"
