

echo "$1"
python sierpinski.py -r split -s 64 --file "$1" > /dev/null &
echo "$2"
python sierpinski.py -r split -s 64 --file "$2" > /dev/null &

python entropy.py --plot -b 1 -x percent -p 128 --file "$1" "$2"