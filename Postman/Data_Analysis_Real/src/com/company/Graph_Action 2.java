package com.company;

import org.knowm.xchart.BitmapEncoder;
import org.knowm.xchart.CategoryChart;
import org.knowm.xchart.CategoryChartBuilder;
import org.knowm.xchart.CategorySeries;
import org.knowm.xchart.style.Styler;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

//creates chart for one sensor data vs time for a session. value is chart filename
public class Graph_Action extends Action{


    String imageName;
    String yAxisTitle;
    ArrayList<String> timestamps;
    TableReader tableReader;


    public Graph_Action(String keyname, int sessionStartID, int sessionEndID, App app,String imageName){
        super(keyname, sessionStartID,sessionEndID, app);
        this.imageName = imageName;
        this.yAxisTitle = app.getSensorTitle(this.keyname);
        this.timestamps = app.getTimestampsForAction(this.keyname, sessionStartID,sessionEndID);
        if(isGraph(keyname)) {
            //just checking to make sure its a graph
        }else{
            System.out.println("ERROR! NOT A GRAPH ACTION");
        }
        this.tableReader = new TableReader();
    }

    //creates chart and sets value = charts filename
    //all data comes in as strings
    public void execute(ArrayList<String> data, String dataType){
        //since data is strings, need to convert them to doubles to graph.
        //As far as I know there is no way to graph strings - this proved to be an inconvenience as it would have been
        //nice to graph brake presses on a graph with other things.
        if(dataType.compareTo("double") == 0) {
            ArrayList<Double> dataDouble = new ArrayList<Double>();
            for (int i = 0; i < data.size(); i++) {
                dataDouble.add(Double.parseDouble(data.get(i)));
            }
            //create chart
            generateChart(this.timestamps, dataDouble, this.yAxisTitle + " vs Time(s)", "Elapsed Time Since Session Start (seconds)", this.yAxisTitle, this.imageName);

            //catches case user puts filename.png or filename
            //just a catch so output filename is always right
            if (this.imageName.contains(".png")) {
                this.value = this.imageName;
            } else {
                this.value = this.imageName + ".png";
            }
        }else{//String for now can't graph so RIP
            System.out.println("ERROR! CAN'T GRAPH STRINGS RIGHT NOW");
            this.value = "ERROR CAN'T GRAPH STRINGS";
        }
    }

    //returns whether the keyname refers to a graph or not
    private boolean isGraph(String keyname){
        ArrayList<Integer> graphIDS = this.app.getGraphActionIDS();

        return graphIDS.contains(this.actionID);
    }

    //creates a .png image of the graph given the parameters, so that the filename can be embedded into the report html
    public void generateChart(ArrayList<String> timestamps, ArrayList<Double> actionData, String chartTitle, String xLabel, String yLabel, String imageFilename){

        // Create Chart
        CategoryChart chart =
                new CategoryChartBuilder()
                        .width(1200)
                        .height(600)
                        .theme(Styler.ChartTheme.GGPlot2)
                        .title(chartTitle)
                        .xAxisTitle(xLabel)
                        .yAxisTitle(yLabel)
                        .build();

        // Customize Chart
        chart.getStyler().setDefaultSeriesRenderStyle(CategorySeries.CategorySeriesRenderStyle.Line);
        //chart.getStyler().setXAxisLabelRotation(-75);
        chart.getStyler().setLegendPosition(Styler.LegendPosition.OutsideE);
        chart.getStyler().setAvailableSpaceFill(0);
        chart.getStyler().setOverlapped(true);


        // Declare data
        List<String> xAxisKeys = timestamps;
        List<Double> yAxisKeys = actionData;

        CategorySeries series =
                chart.addSeries(yLabel, xAxisKeys, yAxisKeys);
        try {
            BitmapEncoder.saveBitmap(chart, imageFilename, BitmapEncoder.BitmapFormat.PNG);
        }catch(IOException ioe){
            ioe.printStackTrace();
        }
    }

    //unused method to set the image name - the chart filename
    public void setImageName(String imageName) {
        this.imageName = imageName;
    }
}
