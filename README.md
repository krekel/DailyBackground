# DailyBackground
A simple python script, with the help of a daily cronjob, will search r/Wallpapers' hot posts, download an image 
and set it as a background.

# Installation
* Donwload script and give permissions ```chmod +x daily_background.py```
* Add the cronjob to the crontab file ```crontab -e```
  ```shell
  0 0 * * * /path/of/script/daily_background.py
  ```
  
## Upcoming Changes
* Identify image formats and add them to the file name
* Download images hosted on imgur(Currently, images hosted on reddit are downloaded)