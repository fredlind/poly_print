for file in $(ls); do
  var0=${file:8:15}
  var="${var0//[^1]}"
  if [[ ${#var} -eq 1 ]]; then
    cp $file $1/Sides2/
  elif [[ ${#var} -eq 2 ]]; then
    cp $file $1/Sides3/
  elif [[ ${#var} -eq 3 ]]; then
    cp $file $1/Sides4/
  elif [[ ${#var} -eq 4 ]]; then
    cp $file $1/Sides5/
  elif [[ ${#var} -eq 5 ]]; then
    cp $file $1/Sides6/
  elif [[ ${#var} -eq 6 ]]; then
    cp $file $1/Sides7/
  fi
done

for directory in $(ls -d $1/*/); do
  echo $directory: $(ls $directory | wc -l)
done