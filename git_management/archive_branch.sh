#!/bin/bash
set -e

echo "Make sure all of your local changes are committed! Otherwise the script will fail. CTRL-C right now and check!!"

read -p "Enter the name of the branch to archive: " BRANCH_NAME

git checkout $BRANCH_NAME 
git tag archive/$BRANCH_NAME
git push origin archive/$BRANCH_NAME --no-verify
git checkout main
git branch -D $BRANCH_NAME          # Local delete
git push origin --delete $BRANCH_NAME --no-verify # Remote delete

echo "$BRANCH_NAME archived!"