package com.unibs.buildingsitepathfinder;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Point;
import android.util.AttributeSet;
import android.view.View;
import android.widget.Button;

@SuppressLint("AppCompatCustomView")
public class CustomButton extends Button implements View.OnClickListener {

    private Point coordinates;
    private String status;
    private GridManager gridManager;

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

    public CustomButton(Context context, GridManager grid) {
        super(context);
        init();
        this.gridManager = grid;
        this.status = "Empty";
    }

    private void init() {
        setOnClickListener(this);
        this.setBackgroundResource(R.drawable.cell_default_button);
        this.setMinimumWidth(50);
        this.setMinimumHeight(50);
    }

    @Override
    public void onClick(View v) {
        gridManager.changeButtonState(this);
        repaint(v);
    }

    /**
     * Update the view according to the status selected by the user
     *
     * @param v the view that has to be updated
     */
    public void repaint(View v) {
        Button btn = (Button) v;
//        btn.setText(this.getStatus());

        if (this.status.equals("Empty")) {
            btn.setBackgroundResource(R.drawable.cell_default_button);
        } else if (this.status.equals("Start")) {
            btn.setBackgroundResource(R.drawable.start_button);
        } else if (this.status.equals("Obstacle")) {
            btn.setBackgroundResource(R.drawable.red_button);
        } else if (this.status.equals("End")) {
            btn.setBackgroundResource(R.drawable.end_button);
        }
    }

    //Getters & Setters
    public Point getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(Point coordinates) {
        this.coordinates = coordinates;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
