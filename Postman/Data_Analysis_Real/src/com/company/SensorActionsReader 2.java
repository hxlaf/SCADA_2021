package com.company;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

//reader associated with the sensor_actions table csv file. Makes it easier to read from the csv file with function calls rather
//than using a bunch of try - catch blocks.
public class SensorActionsReader {
    String csvFile = "sensor_actions_table.csv";
    BufferedReader br;
    int indexID = 0;
    int indexSensorID = 1;
    int indexActionID = 2;
    int indexKey = 3;

    public SensorActionsReader(){
        try{
            br = new BufferedReader(new FileReader(csvFile));
        }catch (IOException ioe){
            ioe.printStackTrace();
        }

    }

    //gets the sensorID (the second column) matching the keyname (the 4th column)
    public String getSensorIDFromKey(String key){
        String output = "";
        String line = "";

        try{
            br = new BufferedReader(new FileReader(csvFile));
            while((line = br.readLine()) !=null){
                String[] row = line.split(",");

                if(row[indexKey].compareTo(key) == 0){
                    output = row[indexSensorID];
                    br.close();
                    break;
                }
            }
        }catch (IOException ioe){
            ioe.printStackTrace();
        }

        return output;
    }
    //gets the actionID (the third column) matching the keyname (4th column)
    public int getActionIDFromKey(String key){
        int output = 0;
        String line = "";
        try{
            br = new BufferedReader(new FileReader(csvFile));
            while((line = br.readLine()) !=null){
                String[] row = line.split(",");
                if(row[indexKey].compareTo(key) == 0){
                    output = Integer.parseInt(row[indexActionID]);
                    br.close();
                    break;
                }
            }
        }catch (IOException ioe){
            ioe.printStackTrace();
        }
        return output;
    }

}
