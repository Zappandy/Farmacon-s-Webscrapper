#!/bin/sh
file=$'edgedriver_win64.zip'
changedir()
{
	work_dir=~/'../../mnt/c/Users/nanoa/PycharmProjects/automateboringstuff/Selenium'
	file_dir=~/'../../mnt/c/Users/nanoa/Downloads/' 
	mv $file_dir$file $work_dir*?;cd $work_dir*?
}
unzipDriver()
{
	unzip edgedriver_win64.zip -d ./Edge_Driver
}
"$@"
