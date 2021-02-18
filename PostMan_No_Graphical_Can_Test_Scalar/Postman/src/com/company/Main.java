package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.io.*;
import java.util.*;

public class Main{

//keeps track of number of chart.pngs created
private static int chartNumber = 1;
//ids associated with where data collection should start and where it should end
private static int sessionStartID = 0;
private static int sessionEndID = 0;

    public static void main(String[] args) {

        //connect to the SQL server, saved to class so don't have to keep reconnecting
        App app = new App();
        app.connect();


        //collect all timestamps for the beginning of sessions from the database
        ArrayList<Date> sessionTimestamps = app.getSessionTimestamps();
        //usableSessionTimestamps is just a copy of sessionTimestamps
        ArrayList<Date> usableSessionTimestamps = sessionTimestamps;
        //change arraylist to array
        String[] sessionsForList = new String[usableSessionTimestamps.size()];

        //generate the list of available sessions to be selected by the user
        for(int i =0;i< usableSessionTimestamps.size();i++){
            if(i<usableSessionTimestamps.size()-1){
                long elapsedTime = usableSessionTimestamps.get(i+1).getTime() -usableSessionTimestamps.get(i).getTime();
                sessionsForList[i] =  "Session" + (i+1) + ": (" + usableSessionTimestamps.get(i) + ") Duration(s): " + elapsedTime/1000;
            }else{
                long elapsedTime = app.getFinalDataTimestamp().getTime() - usableSessionTimestamps.get(i).getTime();
                sessionsForList[i] =  "Session" + (i+1) + ": (" + usableSessionTimestamps.get(i) + ") Duration(s): " + elapsedTime/1000;
            }
        }

        //collect ids for sessions, used to account for the last entry in the data also being the end of the last session
        //the system works with only session beginnings and each session's start is defined by a session ON and ends
        //on the next session ON or the end of database
        ArrayList<Integer> sessionIDS = app.getDataIDForTimestamps();
        int finalID = app.getFinalDataID();
        sessionIDS.add(finalID+1);


        //create the gui
        JComboBox<String> sessionList = new JComboBox<String>((String[]) sessionsForList);
        JFrame list = new JFrame();
        list.add(sessionList, BorderLayout.CENTER);
        sessionList.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent event) {
                JComboBox<String> combo = (JComboBox<String>) event.getSource();
                String selectedSession = (String) combo.getSelectedItem();

                //It is assumed that the session number is the index of sessionIDS +1, so that for
                // Session1, the corresponding session ID is sessionIDS.get(0)
                //the -48 is due to going from ascii to number
                char index;
                int IDIndex = (index = selectedSession.charAt(selectedSession.indexOf(':')-1)) - 1-48;

                //error if somehow the last entry in the data table is the selected session
                // i.e the data table ends in a session ON
                if(sessionIDS.get(IDIndex) == finalID){
                   // System.out.println("Error with session, check if empty session.");
                    System.exit(-1);
                }else
                    //the sessionStartID is +1 because data collection shouldn't start on the session ON entry
                    //it should start at the next data entry
                    sessionStartID = sessionIDS.get(IDIndex)+ 1;

                //the same idea applies for sessionEndID as sessionStartID
                sessionEndID = sessionIDS.get(IDIndex +1)-1;

                //create the selected report based on the given template
                generateReport("summary_template.html","summary.html", sessionStartID, sessionEndID,app);
                System.out.println("Report Generated");

                System.exit(0);

            }
        });
        //sets the size of the scrollable menu
        //would be nice if the menu didn't start at the top left
        list.setSize(400,100);
        list.show();


    }

    //filename must include .html, search for regex and replace with replacement.
    //searches through filename and replaces regex with replacement
    public static void searchAndReplace(String regex, String replacement, String filename) {
        //i got this code online so I'm not 100% sure how it works
        Path path = Paths.get(filename);
        Charset charset = StandardCharsets.UTF_8;

        try {
            String content = new String(Files.readAllBytes(path), charset);
            content = content.replaceAll( regex, replacement);
            Files.write(path, content.getBytes(charset));
        }catch(IOException ioe){
            ioe.printStackTrace();
        }

    }

    //returns arraylist containing the index of each occurrence of c within str
    public static ArrayList<Integer> charIndices(char c, String str){
        ArrayList<Integer> indices = new ArrayList<Integer>();

        for(int i=0; i < str.length(); i++)
        {    if(str.charAt(i) == c)
                indices.add(i);
        }

        return indices;
    }

    //takes line of report html file and returns the actions in that line.
    //returns ["glvv_max:name", "rpm_max:val"] etc
    public static ArrayList<String> getReportLineActions(String line){
        ArrayList<Integer> indices = charIndices('#', line);
        ArrayList<String> reportActions = new ArrayList<String>();

        for(int i =0; i<indices.size(); i++){
            reportActions.add(line.substring(indices.get(i)+1, indices.get(i+1)));
            i++;
        }

        return reportActions;
    }

    //appends appendedList to the end of primaryList
    //way to append arraylists of strings
    public static ArrayList<String> appendArrayList(ArrayList<String> primaryList, ArrayList<String> appendedList){

        ArrayList<String> combinedList = new ArrayList<String>();

        for(int i = 0; i<appendedList.size(); i++) {
            primaryList.add(appendedList.get(i));
        }
        combinedList = primaryList;
        return combinedList;
    }

    //input filename : "test_template.html" output: {etime:name,dist:name,dist:val, ... etc}
    //retrieves the contents of the action tags, the string between #---#
    public static ArrayList<String> getAllReportActions(String filename){

        ArrayList<String> reportActions = new ArrayList<String>();
        BufferedReader reader;
        String line;
        try{
            reader = new BufferedReader(new FileReader(filename));

            while((line = reader.readLine()) != null){
                appendArrayList(reportActions,getReportLineActions(line));
            }

        }catch(IOException ioe){
            ioe.printStackTrace();
        }
        return reportActions;
    }

    //copy the contents from one file to another
    public static void copyFile(String originalFile, String copiedFile){

        try {
            FileReader fr = new FileReader(originalFile);
            BufferedReader br = new BufferedReader(fr);
            FileWriter fw = new FileWriter(copiedFile, true);
            String s;

            while ((s = br.readLine()) != null) { // read a line
                fw.write(s + "\n"); // write to output file
                fw.flush();
            }
            br.close();
            fw.close();
            System.out.println("file copied");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //checks whether the keyname refers to a scalar action
    //the actions table keeps track of the type of output associated with each action and consequently each keyname
    public static boolean isScalar(String keyname, App app){
        ArrayList<Integer> scalarIDS = app.getScalarActionIDS();
        int actionID = app.getActionID(keyname);

        return scalarIDS.contains(actionID);
    }

    //checks whether the keyname refers to a graph action
    public static boolean isGraph(String keyname, App app){
        ArrayList<Integer> graphIDS = app.getGraphActionIDS();
        int actionID = app.getActionID(keyname);

        return graphIDS.contains(actionID);
    }

    //creates list of trees with their children added.
    //pretty much creates a list of structures that hold a sensor and actions associated with the sensor data
    public static ArrayList<CollectionList> getCollectionLists(ArrayList<String> reportActions,int sessionStartID, int sessionEndID, App app){
        ArrayList<String> actionValues = new ArrayList<String>();
        ArrayList<CollectionList> collectionLists = new ArrayList<CollectionList>();

        String sensorAction;
        String entry;
        int deliminatorIndex;
        Collector tempCollector;

        //input parameter was list {glvv_max:name, rpm_min:name,...etc}
        //for each action in the above list, it is reduced to glvv_max, rpm_min, etc.
        //and handle creating a tree for the sensor corresponding to the action or if the tree for the sensor
        //already exists, just add the action to the corresponding list of children for the tree.
        for(int i =0; i<reportActions.size(); i++){
            entry = reportActions.get(i);
            deliminatorIndex = entry.indexOf(':');
            //the shorted action tag -> glvv_max
            sensorAction = entry.substring(0,deliminatorIndex);
            //boolean used to not add duplicate children to a tree
            boolean sensorExists = false;

            //check each tree to see if they already have collector for sensor given by sensor action
            for(int j = 0; j< collectionLists.size();j++) {
                //if the collector for sensor already exists
                if(collectionLists.get(j).getParent().sensorName.compareTo(app.getSensorNameForAction(sensorAction)) == 0) {
                    //if it does, don't create a tree for the sensor
                    sensorExists = true;
                    break;
                }

            }

            //if a tree/collector already exists for the sensor associated with the action,
            //just add the action to the list of children for the tree
            if(sensorExists) {
                addChildToCollectionList(collectionLists,sensorAction,app);
                continue;
            }else {
                //if collector for sensor doesn't exist, create tree that holds that sensor collector
                collectionLists.add(new CollectionList(new Collector(sensorAction,sessionStartID, sessionEndID,app)));
                //then add the child action to the tree
                addChildToCollectionList(collectionLists,sensorAction,app);
            }


            }
        return collectionLists;

        }

    //adds child corresponding to reportAction to correct Tree within list of Trees, doesn't allow for duplicate actions
    //reportAction is like glvv_max
    public static void addChildToCollectionList(ArrayList<CollectionList> collectionLists, String reportAction, App app){

        //get sensor for action
        String actionSensor = app.getSensorNameForAction(reportAction);
        boolean duplicate = false;

        //go through each collectionList and look for sensor match
        for(int i =0; i<collectionLists.size(); i++){
            //make sure action isn't already a child
            //for each child check if the reportAction keyname exists
            for(int j = 0;j<collectionLists.get(i).getChildren().size();j++){
                //if reportAction keyname matches or graph3 exists, don't add duplicate child
//                if(collectionLists.get(i).getChildren().get(j).keyname.compareTo(reportAction) ==0 ||  (collectionLists.get(i).graph3 != null && collectionLists.get(i).graph3.keyname.compareTo(reportAction) == 0)){ //**source of error
//                    duplicate = true;
//                    break;
//                }
            }
            //stop if action is a duplicate
            if(duplicate){
                break;
            }

            //if match action to current tree (we are still in a for loop through the tree list)
            if(collectionLists.get(i).getSensorName().compareTo(actionSensor) == 0){

                //if Scalar
                if(isScalar(reportAction,app)){
                    collectionLists.get(i).addChild(new Scalar_Action(reportAction,sessionStartID,sessionEndID,app));
                }
                //else if (isGraph(reportAction,app)){
//                // if Graph
//                    //filename and chartnumber are used to create the filename for each graph so that naming
//                    //doesn't have to accounted for directly
//                    String filename = "Chart_" + chartNumber;
//                    chartNumber++;
//                    collectionLists.get(i).addChild(new Graph_Action(reportAction,sessionStartID,sessionEndID,app,filename));
//                }else{
//                //if graph3
//                    String filename = "Chart_" + chartNumber;
//                    chartNumber++;
//                    TableReader tr = new TableReader();
//                    int sensorID1 = tr.getGraph3SensorID1(reportAction);
//                    int sensorID2 = tr.getGraph3SensorID2(reportAction);
//                    int sensorID3 = tr.getGraph3SensorID3(reportAction);
//                    collectionLists.get(i).setGraph3(sensorID1,sensorID2,sensorID3,sessionStartID,sessionEndID,filename,reportAction,app);
//
//                }

            }else{
                //the reportAction's corresponding sensor doesn't match to the current collectionLists's collector
                continue;
            }
        }

    }

    //execute each action in every tree
    //go through each tree and execute every action in the list of actions and execute the graph3 if it exists
    //within a tree
    public static void executeActions(ArrayList<CollectionList> trees){
        for(int i =0;i<trees.size();i++){
            CollectionList currentList = trees.get(i);
            for(int j = 0;j<trees.get(i).getChildren().size();j++){
                currentList.getChildren().get(j).execute(currentList.getCollectionListData(),currentList.getParent().dataType);
//                if(currentList.containsGraph3){
//                    currentList.graph3.execute();
//                }
            }
        }
    }

    //filename must include .html, create html to be viewed. Copy template, replace tags with values.
    public static void insertData(String filenameTemplate, String filenameReport, ArrayList<CollectionList> collectionLists){
        try{
            //create report file
            File report = new File(filenameReport);
            if(report.createNewFile()){
                System.out.println("file created");
            }else{
                PrintWriter pw = new PrintWriter(filenameReport);
                pw.close();
            }
            //copy template into report file so that can search/replace tags with names/values
            copyFile(filenameTemplate,filenameReport);


            //replace all tags with names/values
            //for each tree
            for(int i =0;i<collectionLists.size(); i++){

                CollectionList currentList = collectionLists.get(i);

                //insert data associated with the graph3 into the file
//                if(currentList.containsGraph3){
//                    searchAndReplace("#" + currentList.graph3.keyname + ":name#",currentList.graph3.actionName, filenameReport);
//                    searchAndReplace("#" + currentList.graph3.keyname + ":val#",currentList.graph3.value, filenameReport);
//                }
                //for each action, insert associated data into the report
                for(int j = 0; j<currentList.getChildren().size();j++){
                    searchAndReplace("#" + currentList.getChildren().get(j).keyname + ":name#",currentList.getChildren().get(j).actionName, filenameReport);
                    searchAndReplace("#" + currentList.getChildren().get(j).keyname + ":val#",currentList.getChildren().get(j).value, filenameReport);

                }

            }
        }catch(IOException ioe){
            ioe.printStackTrace();
        }

    }

    //create the specified report based on on the template given
    public static void generateReport(String templateFilename, String reportFilename, int sessionStartID, int sessionEndID ,App  app){
        //get all action reports
        ArrayList<String> reportActions = getAllReportActions("summary_template.html");
        ArrayList<CollectionList> collectionLists = new ArrayList<CollectionList>();
        //get and fill collectionLists
        collectionLists = getCollectionLists(reportActions,sessionStartID,sessionEndID, app);
        //execute each action - get values and names for each action/sensor
        executeActions(collectionLists);
        //insert the collected data into the report
        insertData(templateFilename,reportFilename,collectionLists);
    }

    }













