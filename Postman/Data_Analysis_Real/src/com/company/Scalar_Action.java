package com.company;

import java.util.ArrayList;
import java.util.Collections;

//Type of action, used for actions with scalar values. Right now that includes max, min, avg, etc.
public class Scalar_Action extends Action{

    ArrayList<String> timestamps;

    public Scalar_Action(String keyname, int sessionStartID, int sessionEndID, App app){
        super(keyname,sessionStartID,sessionEndID, app);
        //check to make sure its a scalar action, there's no real catch here right now, but could add one
        //just prints a message if there's an issue
        if(isScalar(keyname)) {
            //just checking to make sure its a scalar
        }else{
            System.out.println("ERROR! NOT A SCALAR ACTION");
        }

        this.timestamps = app.getTimestampsForAction(this.keyname, sessionStartID,sessionEndID);
    }

    //sets value to result of applying scalar function to dataset
    //e.g max -> 16.32
    //results are String even though they are double, because they are going in an html file and I assumed they need to
    //be strings. Not sure if they actually do or not
    public void execute(ArrayList<String> data, String dataType){
        //check if the data type is actually double , not string
        if(dataType.compareTo("double") == 0) {
            // convert string data to double data
            ArrayList<Double> dataDouble = new ArrayList<Double>();
            for(int i = 0; i<data.size(); i++){
                dataDouble.add(Double.parseDouble(data.get(i)));
            }
            //go through switch of possible scalar actions
            switch (this.actionID) {
                    //max
                case 1:
                    if (data.size() == 1) {
                        this.value = Double.toString(dataDouble.get(0));
                    } else {
                        this.value = Double.toString(Collections.max(dataDouble));
                    }
                    break;
                    //min
                case 2:
                    this.value = Double.toString(Collections.min(dataDouble));
                    break;
                    //avg - time average to be more specific
                case 3:
                    ArrayList<Double> doubleList = new ArrayList<Double>();
                    for(int i =0;i<timestamps.size();i++){
                        doubleList.add(Double.parseDouble(timestamps.get(i)));
                    }
                    //time average based around function: 1/period * integral(f(t)dt) over period
                    //found at: https://astronomy.swin.edu.au/cosmos/T/Time+Average
                    this.value = Double.toString(integralApproximation(dataDouble,doubleList)/(doubleList.get(doubleList.size()-1) - doubleList.get(0)));
                    break;
                default:
                    this.value = "Action either not listed or not scalar.";
                    break;

            }
        }else{//not a double data type - a string
            System.out.println("ERROR, PASSING A SENSOR WITH NON DOUBLE DATA AS SCALAR ACTION");
            this.value = "ERROR";

        }
    }

    //returns whether the keyname refers to a scalar action
    public boolean isScalar(String keyname){
        ArrayList<Integer> scalarIDS = this.app.getScalarActionIDS();

        return scalarIDS.contains(this.actionID);
    }

    //approximate integral of function based on (x,y) values
    //uses trapezoidal approximation of integral found here:
    //https://www.mathsisfun.com/calculus/integral-approximations.html
    public static double integralApproximation(ArrayList<Double> yValues, ArrayList<Double> xValues){
        double currentIntegral = 0;
        for(int i=0;i<yValues.size()-1;i++){
            currentIntegral = currentIntegral + (((yValues.get(i) + yValues.get(i+1))/2)*(xValues.get(i+1)-xValues.get(i)));
        }
        return currentIntegral;
    }

}
