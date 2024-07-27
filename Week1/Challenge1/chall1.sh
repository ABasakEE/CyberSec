#!/usr/bin/env bash
shopt -s extglob

#create a config file to record the events

config="config.txt"
touch "$config"

#starting with off with chall1.7z

7z e chall1.7z
echo "Unzipped main 7z folder" >> "$config"
rm chall1.7z 

#extracting the password

#get the file without extension name
flag=1



while [[ "$flag" -ne 0 ]]; do 
    #check which file name doesn't have an extension 
    #we need to extract password from that
    pass=$(find !(*.*))
    
    #what file format to unzip
    zip_flag=0
    zip_file=0
    sevenz_file=0

    if [[ $(find -- *.zip | wc -l) -eq 1 ]]; then
        zip_flag=1
        zip_file=$(find -- *.zip)
        echo "$zip_file" >> "$config"
    elif [[ $(find -- *.7z | wc -l) -eq 1 ]]; then
        zip_flag=2
        sevenz_file=$(find -- *.7z)
        echo "$sevenz_file" >> "$config"
    else
        echo "Nothing found" >> "$config"
        break
    fi
    
    #perform the encodings 
    #try every pattern


    p1=$(base64 "$pass") #base64 encoding
    p2=$(base32 "$pass") #base32 encoding
    p3=$(xxd -p "$pass") #hex dump


    if [[ "$zip_flag" -eq 1 ]]; then #try with the unzip command
        try1=$(unzip -P "$p1" "$zip_file")
        if ! $try1; then
            echo "Base64 encoding did not work" >> "$config"

            try2=$(unzip -P "$p2" "$zip_file")

            if ! $try2 ; then
                echo "Base32 encoding did not work" >> "$config"

                try3=$(unzip -P "$p3" "$zip_file")

                if ! $try3 ; then 
                    echo "Hexadecimal encoding did not work" >> "$config"

                    text=$(<"$pass")
                    unzip -P "$text" "$zip_file"

                else
                    echo "Hexadecimal encoding worked" >> "$config"
                fi
            else 
                echo "Base32 encoding worked" >> "$config"
            fi
        else
            echo "Base64 encoding worked" >> "$config" 
        fi

        rm "$zip_file" #remove the file to prevent future issues
    
    else
        try1=$(7z x "$sevenz_file" -p"$p1")
        if ! $try1 ; then
            echo "Base64 encoding did not work" >> "$config"

            try2=$(7z x "$sevenz_file" -p"$p2")

            if ! $try2 ; then
                echo "Base32 encoding did not work" >> "$config"

                try3=$(7z x "$sevenz_file" -p"$p3")

                if ! $try3 ; then 
                    echo "Hexadecimal encoding did not work" >> "$config"

                    text=$(<"$pass")
                    7z x "$sevenz_file" -p"$text"
                else
                    echo "Hexadecimal encoding worked" >> "$config"
                fi
            else 
                echo "Base32 encoding worked" >> "$config"
            fi
        else
            echo "Base64 encoding worked" >> "$config"
        fi

        rm "$sevenz_file" #remove the file to prevent future issues    
    fi

    rm "$pass" #remove the file containing password
    
    pass=$(ls -1 !(*.*))
    if grep -q "flag" "$pass"; then
        echo "Flag found" >> "$config"
        flag=1
    fi
done





