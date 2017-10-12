#!/bin/bash
echo -e "\033[33m hello lisen! this is your cp shell script \033[0m"
read -p "input DevDir:" DevDir
read -p "input GithubDir:" GithubDir
rm -r $GithubDir
cp -r $DevDir $GithubDir
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
