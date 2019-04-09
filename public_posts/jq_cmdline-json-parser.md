% Title:       jq Commandline JSON Data Parser
% Author:      Xiaoxue Wang<xxwjoy@hotmail.com>
% Date:        2019-04-09

## jq intro

Display JSON data with a beauty format.

https://stedolan.github.io/jq/
jq is like sed for JSON data - you can use it to slice and filter and map and transform structured data with the same ease that sed, awk, grep and friends let you play with text.

## Usage
`cat filea | jq . > filea-jq`

## Install rpm jq in fedora29
~~~
╭[localhost] ~/Work/handy-tools/redhat-insights-related/taoism-reviewd-kcs-analysis (ADD-KCS-status-plugin-status-sync-check-to-taoism)
╰> sudo yum provides jq
Last metadata expiration check: 0:39:41 ago on Tue 09 Apr 2019 10:02:32 AM CST.
jq-1.5-13.fc29.i686 : Command-line JSON processor
Repo        : fedora
Matched from:
Provide    : jq = 1.5-13.fc29

jq-1.5-13.fc29.x86_64 : Command-line JSON processor
Repo        : fedora
Matched from:
Provide    : jq = 1.5-13.fc29

╭[localhost] ~/Work/handy-tools/redhat-insights-related/taoism-reviewd-kcs-analysis (ADD-KCS-status-plugin-status-sync-check-to-taoism)
╰> sudo yum install jq
Last metadata expiration check: 0:39:55 ago on Tue 09 Apr 2019 10:02:32 AM CST.
Dependencies resolved.
=============================================================================================================================================================================
 Package                                   Arch                                   Version                                      Repository                               Size
=============================================================================================================================================================================
Installing:
 jq                                        x86_64                                 1.5-13.fc29                                  fedora                                  159 k
Installing dependencies:
 oniguruma                                 x86_64                                 6.9.1-1.fc29                                 updates                                 188 k
...
~~~
