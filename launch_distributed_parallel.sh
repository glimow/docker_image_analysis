for process in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
	ipython main.py ./images.txt ./packages $process 16 &
done
