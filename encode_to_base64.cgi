#!/bin/bash

function urlencode {

  local url_encoded="${1//+/ }"
  printf '%b' "${url_encoded//%/\\x}"

}

[ -z "$POST_STRING" -a "$REQUEST_METHOD" == "POST" -a ! -z "$CONTENT_LENGTH" ] && read -n $CONTENT_LENGTH POST_STRING

#alternate temporary the default Internal Field Separator, standard IFS is a whitespace (space, tab, newline)
OIFS=$IFS
IFS='=&'

#Array variables created using compound assignments
parm_get=($QUERY_STRING)
parm_post=($POST_STRING)

#restore original Internal Field Separator
IFS=$OIFS

#Explicit declaration of arrays
declare -A get
declare -A post

# compose "get" associative array
for ((i=0; i<${#parm_get[@]}; i+=2)); do
  get[${parm_get[i]}]=$(urlencode ${parm_get[i+1]})
done

# compose "post" associative array
for ((i=0; i<${#parm_post[@]}; i+=2)); do
  post[${parm_post[i]}]=$(urlencode ${parm_post[i+1]})
done

#encoding the input
encoded_text=$(echo ${post[to_be_encoded_text]} | openssl base64)

#the html code
echo "Content: text/html"
echo
cat <<EOT
<!DOCTYPE html>
<html>
<head></head>
<body>
Dear <b>${post[title]} ${post[name]}</b>, please find your Base64 encoded string below.
<br>
<hr>
<br>
<p><b>${encoded_text}</b></p>
<br>
<a href="/encode_to_base64.html">BACK</a>
</body>
</html>
EOT
