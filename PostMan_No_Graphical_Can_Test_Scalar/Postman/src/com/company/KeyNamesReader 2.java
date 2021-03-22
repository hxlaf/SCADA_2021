package com.company;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

//reader associated with the key_names table csv file. Makes it easier to read from the csv file with function calls rather
//than using a bunch of try - catch blocks.
public class KeyNamesReader {
    String csvFile = "key_names_table.csv";
    BufferedReader br;
    int indexKey = 0;
    int indexName = 1;

    public KeyNamesReader(){
        try{
            br = new BufferedReader(new FileReader(csvFile));
        }catch (IOException ioe){
            ioe.printStackTrace();
        }

    }
    //provide a key/keyname gets back the chart-ready, legible title.
    //e.g glvv_max -> Max GLVV (V)
    public String getNameFromKey(String key){
        String output = "";
        String line = "";
        try{
            br = new BufferedReader(new FileReader(csvFile));
            while((line = br.readLine()) !=null){
                String[] row = line.split(",");
                if(row[indexKey].compareTo(key) == 0){
                    output = row[indexName];
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
