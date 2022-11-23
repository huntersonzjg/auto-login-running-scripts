#!/bin/bash
gw1=192.168.65.2   
gw2=192.168.65.61
(
while :      
do
        route del default
        route add default gw $gw1    
        while ping -c 1 $gw1 &> /dev/null 
                do
                        sleep 5  
                done              
        route del default 
        route add default gw $gw2   
        until ping -c 1 $gw1 &> /dev/null  
                do
                        sleep 5
                done  
done
) 