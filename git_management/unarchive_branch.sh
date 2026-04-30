#!/bin/bash
set -e

echo "Make sure all of your local changes are committed! Otherwise the script will fail. CTRL-C right now and check!!"

read -p "Enter the name of the branch to un-archive: " BRANCH_NAME

git checkout -b $BRANCH_NAME archive/$BRANCH_NAME
git push origin $BRANCH_NAME --no-verify
git tag -d archive/$BRANCH_NAME
git push origin --delete archive/$BRANCH_NAME --no-verify

echo "$BRANCH_NAME un-archived!"
