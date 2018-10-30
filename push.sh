#!/bin/bash
echo "hello lisen! this is your push shell script"
read -p "input GithubDir:" GithubDir
cd $GithubDir
git pull
git status
while true
do
    read -p "input adding file:" file
    if  [ ! -n "$file" ] ;then
        echo "Adding file end"
        break
    else
        git add $file
git status
fi
done
git status
IFS="|"
read -p "input commitString:" commitString
git commit -m $commitString
read -p "input remote branch:" remote_branch
git push origin $remote_branch