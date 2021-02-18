package com.company;

import java.util.ArrayList;

//reader associated with all the csv files. Makes it easier to read from the csv files, rather than calling each reader
//for each file, can just call this one and the data you want
//contains a bunch of functions which retrieve specific types of information from the csv files, usually based on the keyname for an action
public class TableReader {
     ActionsTableReader actionsTableReader;
     KeyNamesReader keyNamesReader;
     SensorActionsReader sensorActionsReader;


    public TableReader(){
        actionsTableReader = new ActionsTableReader();
        keyNamesReader = new KeyNamesReader();
        sensorActionsReader = new SensorActionsReader();
    }

    //return name of action, the legible/chart/title name
    public String getActionName(String keyname){
        return keyNamesReader.getNameFromKey(keyname);
    }

    //return action id based on keyname
    public int getActionID(String keyname){
        return sensorActionsReader.getActionIDFromKey(keyname);
    }

    //return the action ids of all actions whose type is scalar
    public ArrayList<Integer> getScalarActionIDS(){
        return actionsTableReader.getScalarActionIDS();
    }
    //return the action ids of all actions whose type is graph
    public ArrayList<Integer> getGraphActionIDS(){
        return actionsTableReader.getGraphActionIDS();
    }

    //get action name from action table based on a keyname
    public String getActionIdentifier(String keyname){

        int actionID = sensorActionsReader.getActionIDFromKey(keyname);
        return actionsTableReader.getActionNameFromID(actionID);
    }

    public int getNumberOfGraphs(int actionID){
        int numberOfGraphs = actionsTableReader.getNumberOfGraphs(actionID);
        return numberOfGraphs;
    }

    //get 1st sensor id for the graph3
    public int getGraph3SensorID1(String keyname){
        return actionsTableReader.getGraphSensorID1(sensorActionsReader.getActionIDFromKey(keyname));
    }
    //get 2nd sensor id for the graph3
    public int getGraph3SensorID2(String keyname){
        return actionsTableReader.getGraphSensorID2(sensorActionsReader.getActionIDFromKey(keyname));
    }
    //get 3rd sensor id for the graph3
    public int getGraph3SensorID3(String keyname){
        return actionsTableReader.getGraphSensorID3(sensorActionsReader.getActionIDFromKey(keyname));
    }
}
