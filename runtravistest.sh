#!/bin/bash

#quick way to grab the travis tests for offline testing...
sed -n  '/#offlinetestingstring/,$p' .travis.yml |tail -n+3|sed 's/^..//'| sed '/^#/ d'|sed 's/^..//'
