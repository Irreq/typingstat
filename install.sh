#!/bin/sh

# bool function to test if the user is root or not (POSIX only)
is_user_root () { [ "$(id -u)" -eq 0 ]; }

if ! is_user_root; then
    echo 'You need root access!'
    echo 'Run: sudo ./install.sh'
    exit 0 # implicit, here it serves the purpose to be explicit for the reader
fi

printf "Type 'yes' to continue installation " >&2
read -r option

echo $option

if test "$option" != "yes"; then
  echo "You need to be certain with what you are doing. Abborting..."
  exit 0
fi

# The path where the main project reside
home_user_path=${PWD%/*/*}

user=${home_user_path##*/}

# Check if user config path exists
if ! [ -d $home_user_path/.config/typingstat ]; then
  echo "Creating config directory: " $home_user_path/.config/typingstat
  mkdir -p $home_user_path/.config/typingstat
fi
if ! [ -f $home_user_path/.config/typingstat/config.py ]; then
  echo "Creating user config file: " $home_user_path/.config/typingstat/config.py
  cp data/default_config.py $home_user_path/.config/typingstat/config.py
  chown -R $user:$user $home_user_path/.config/typingstat/config.py
fi

DIR=/etc/typingstat
if ! [ -d "$DIR" ]; then
    echo "Creating daemon config directory: " /etc/typingstat
    mkdir -p $DIR
fi

FILE=/etc/typingstat/config.py
if ! [ -f "$FILE" ]; then
    echo "Linking daemon config file: " /etc/typingstat/config.py " from " $home_user_path/.config/typingstat/config.py
    ln $home_user_path/.config/typingstat/config.py /etc/typingstat/config.py
fi

FILE=/usr/bin/typingstatd
if ! [ -f "$FILE" ]; then
    echo "Copying daemon file: 'typingstatd' to " $FILE
    cp typingstatd $FILE
fi

cat NOTICE
