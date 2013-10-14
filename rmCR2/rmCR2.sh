#!/bin/bash
#Copyleft rom.cpp@gmail.com

pictures_dir=~/Pictures
trash_files_dir=~/.local/share/Trash/files
trash_info_dir=~/.local/share/Trash/info
CR2_filename=IMG_????.CR2
JPG_filename=IMG_????.JPG

# Remove .CR2 files in the Pictures directory
#  if .JPG file not found.
if [ -d ${pictures_dir} ]; then
    for cr2_file in ${pictures_dir}/${CR2_filename}; do
        if [ -e $file ]; then
            jpg_file=${cr2_file}
            jpg_file=${jpg_file%.CR2}.JPG
            if [ ! -e ${jpg_file} ]; then
                rm $cr2_file
            fi
        fi
    done
fi

# Remove .CR2 and .JPG files in the Trash/files directory.
if [ -d ${trash_files_dir} ]; then
    for file in ${trash_files_dir}/${CR2_filename}; do
        if [ -e $file ]; then
            rm $file
        fi
    done
    for file in ${trash_files_dir}/${JPG_filename}; do
        if [ -e $file ]; then
            rm $file
        fi
    done
fi

# Remove .CR2 and .JPG files' info in the Trash/info directory.
if [ -d ${trash_info_dir} ]; then
    for file in ${trash_info_dir}/${CR2_filename}.trashinfo; do
        if [ -e $file ]; then
            rm $file
        fi
    done
    for file in ${trash_info_dir}/${JPG_filename}.trashinfo; do
        if [ -e $file ]; then
            rm $file
        fi
    done
fi

