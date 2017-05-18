#! /bin/bash 

# default
SIZEGB=1
SIZEMB=1000000

manageDir()
{
  if [ $(du Pictures/reddit_wp/ | awk '{print $1}') -gt $1 ]
  then
      rm Pictures/reddit_wp/*
  fi
}


# only handles integers
if [ $1 -eq 0 ]
then 
    # function with default
    manageDir $SIZEMB
elif [ $1 -gt $SIZEGB ]
then    
    # function with custom size
    MAX_SIZE=$[$1 \* 1000000]
    echo $MAX_SIZE

    manageDir $MAX_SIZE
else
    manageDir $SIZEMB
   
fi
