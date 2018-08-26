package com.unibs.buildingsitepathfinder;

import android.annotation.SuppressLint;
import android.support.constraint.ConstraintLayout;
import android.view.View;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;

public class GridManager {
    private ArrayList<CustomButton> map;
    private int size;
    private int obstacles;
    private boolean isStartSet;
    private boolean isEndSet;
    private HashMap<String, String> conversionMap;

    private CustomButton startButton;
    private CustomButton endButton;
    private ConstraintLayout gridView;
    private TextView obstaclesCounter, robotPosition, targetPosition;


    public GridManager(ArrayList<CustomButton> gridButtons, ConstraintLayout grid, int size, TextView obstaclesCounter,
                       TextView robotPosition, TextView targetPosition) {
        this.isEndSet = false;
        this.isStartSet = false;
        this.map = gridButtons;
        this.gridView = grid;
        this.size = size;
        this.obstacles = 0;
        this.obstaclesCounter = obstaclesCounter;
        this.robotPosition = robotPosition;
        this.targetPosition = targetPosition;

        //Labels init
        this.targetPosition.setText("[?,?]");
        this.robotPosition.setText("[?,?]");
        this.obstaclesCounter.setText(String.valueOf(this.obstacles));

        //Conversion map init
        this.conversionMap = new HashMap<>();
        this.conversionMap.put("Empty", "_");
        this.conversionMap.put("Obstacle", "X");
        this.conversionMap.put("Start", "S");
        this.conversionMap.put("End", "E");
    }

    /**
     * Changes the state of a button according to a FSM
     *
     * @param cb the button that had been pressed
     */
    @SuppressLint("SetTextI18n")
    public void changeButtonState(CustomButton cb) {
        if (cb.getStatus().equals("Empty")) {
            cb.setStatus("Obstacle");
            this.obstacles++;

        } else if (cb.getStatus().equals("Obstacle")) {
            if (this.isEndSet) {
                this.endButton.setStatus("Empty");
                this.endButton.repaint(this.gridView.getViewById(endButton.getId()));
            }

            cb.setStatus("End");
            this.isEndSet = true;
            this.endButton = cb;
            this.targetPosition.setText("[" + endButton.getCoordinates().x + "," + endButton.getCoordinates().y + "]");
            this.obstacles--;

        } else if (cb.getStatus().equals("End")) {
            this.isEndSet = false;

            if (this.isStartSet) {
                this.startButton.setStatus("Empty");
                this.startButton.repaint(this.gridView.getViewById(startButton.getId()));
                this.robotPosition.setText("[?,?]");
            }
            cb.setStatus("Start");
            this.isStartSet = true;
            this.startButton = cb;
            this.robotPosition.setText("[" + startButton.getCoordinates().x + "," + startButton.getCoordinates().y + "]");

        } else {
            cb.setStatus("Empty");
            this.robotPosition.setText("[?,?]");
            this.isStartSet = false;
        }
        this.obstaclesCounter.setText(String.valueOf(obstacles));
    }


    public String convertToMazeMap() {
        if (!this.isComplete())
            return "";

        StringBuilder sb = new StringBuilder();
        int currentRow, previousRow = 0;

        for (CustomButton cb : this.map) {
            currentRow = cb.getCoordinates().x;

            if (currentRow > previousRow)
                sb.append("\n");
            previousRow = currentRow;

            switch (cb.getStatus()) {
                case "Empty":
                    sb.append("_ ");
                    break;
                case "Start":
                    sb.append("S ");
                    break;
                case "End":
                    sb.append("E ");
                    break;
                case "Obstacle":
                    sb.append("X ");
                    break;
            }
        }

        return sb.toString();
    }

    private boolean isComplete() {
        return this.isEndSet() && this.isStartSet();
    }

    // Getters and setters
    private boolean isStartSet() {
        for (CustomButton cb : this.map) {
            if (cb.getStatus().equals("Start"))
                return true;
        }
        return false;
    }

    private boolean isEndSet() {
        for (CustomButton cb : this.map) {
            if (cb.getStatus().equals("End"))
                return true;
        }
        return false;
    }

    public CustomButton getStartButton() {
        for (CustomButton cb : this.map) {
            if (cb.getStatus().equals("Start"))
                return cb;
        }
        return null;
    }

    public void displayStartingOrientation(String orientation, int viewId) {
        View sb = this.gridView.findViewById(viewId);

        if (orientation.equals("North"))
            sb.setBackgroundResource(R.drawable.arrow_up_bold_box_outline);
        else if (orientation.equals("South"))
            sb.setBackgroundResource(R.drawable.arrow_down_bold_box_outline);
        else if (orientation.equals("East"))
            sb.setBackgroundResource(R.drawable.arrow_right_bold_box_outline);
        else if (orientation.equals("West"))
            sb.setBackgroundResource(R.drawable.arrow_left_bold_box_outline);
    }
}
