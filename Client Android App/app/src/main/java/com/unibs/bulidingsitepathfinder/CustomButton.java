package com.unibs.bulidingsitepathfinder;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Color;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;
import android.widget.Button;

@SuppressLint("AppCompatCustomView")
public class CustomButton extends Button implements View.OnClickListener {

    private int[] coordinates = new int[2];
    private String status;

    public CustomButton(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        init();
        this.status = "Empty";
    }

    public CustomButton(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
        this.status = "Empty";
    }

    public CustomButton(Context context) {
        super(context);
        init();
        this.status = "Empty";
    }

    private void init() {
        setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        // Update the state according to the FSM
        if (status == "Empty") {
            status = "Obstacle";
        } else if (status == "Obstacle") {
            status = "Start";
        } else if (status == "Start") {
            status = "Empty";
        }

        // Update color
        repaint(v);
    }

    /**
     * Update the view according to the status selected by the user
     *
     * @param v the view that has to be updated
     */
    public void repaint(View v) {
        if (this.status == "Empty") {
            //obstacle
            v.setBackgroundColor(Color.RED);
        } else if (this.status == "Obstacle") {
            //start
            v.setBackgroundColor(Color.GREEN);
        } else if (this.status.equals("Start")) {
            //empty
            v.setBackgroundColor(Color.CYAN);
        }

        Log.d("Color updated", "Color updated!");
    }

    //Getters & Setters
    public int[] getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(int[] coordinates) {
        this.coordinates = coordinates;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
