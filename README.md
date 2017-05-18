# DailyBackground
A simple python script, with the help of a daily cronjob, will search r/Wallpapers' hot posts, download an image 
and set it as a background.

# Installation
* Donwload script and give permissions ```chmod +x daily_background.py```
* Add cronjobs to the crontab file ```crontab -e```
  ```shell
  0 0 * * * /path/of/script/daily_background.py
  0 0 1 * * /path/of/script/dir_manager.sh 0 # Will run the first day of every month. Change if needed.
  ```
### Dir Manager
This simple shell script will delete every wallpaper in the directory once it reaches the maximum size specified.

By default is set to every 1GB.

```shell
 dir_manager.sh 0 # Default 1GB
 dir_manager.sh 2 # 2GB
  ```
