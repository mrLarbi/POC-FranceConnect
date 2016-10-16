cd services

which python2 >& /dev/null
rc=$?
if [ $rc != 0 ]
then
    echo "Error : python 2 needs to be installed" >&2
    exit 1
fi

python2 main.py
