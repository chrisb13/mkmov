#borrowed from:
#https://gist.github.com/lbergelson/4265e5ef3ec8b60dac97

#this was found here:
#https://github.com/github/git-lfs/issues/598

#could also look at the following stackoverflow question...
#"How to use Git LFS with Travis-CI (error building R data "

#and possibly: 
#http://stackoverflow.com/questions/tagged/git-lfs
#https://travis-ci.org/github/git-lfs

#see here, for official documentation: https://github.com/github/git-lfs

#!/bin/bash
echo "cloning"
#git clone git@github.com:github/git-lfs.git
git clone https://github.com/github/git-lfs.git $(pwd)/mkmovexamples/git-lfs

echo "cd into git-lfs"
cd $(pwd)/mkmovexamples/git-lfs

echo "checkout commit 4457d7c7c5906025f753579f67f975792235b717"
git checkout 4457d7c7c5906025f753579f67f975792235b717

echo "scripts/bootstrap"
script/bootstrap

echo "ls bin"
ls bin

echo "cd back down"
cd ..

echo "installl"
#git-lfs/bin/git-lfs init #old line
git-lfs/bin/git-lfs install

echo "pull"
#git-lfs/bin/git-lfs fetch #old line
git-lfs/bin/git-lfs pull
