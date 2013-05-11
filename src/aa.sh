#!/bin/bash - 
#===============================================================================
#
#          FILE:  aa.sh
# 
#         USAGE:  ./aa.sh 
# 
#   DESCRIPTION:  i
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: YOUR NAME (), 
#       COMPANY: 
#       CREATED: 2013/05/11 18时25分27秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
echo $@

python /usr/local/bin/wiznotecli.py <<EOF $@ EOF
