if [ "$EUID" -ne 0 ]
then 
    echo "Error : Must be run as root"
    exit 1
fi

which pip2 >& /dev/null
rc=$?
if [ $rc != 0 ]
then
    echo "Error : pip2 needs to be installed" >&2
    exit 2
fi

pip2 install -r requirements.txt
rc=$?
if [ $rc != 0 ]
then
    echo "Error : Failed to install dependecies" >&2
    exit 3
fi
