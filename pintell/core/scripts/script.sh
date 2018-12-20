for file in *.txt
do
    dir="${file%.txt}"
    mkdir -- "$dir"
    mv -- "$file" "$dir"
done