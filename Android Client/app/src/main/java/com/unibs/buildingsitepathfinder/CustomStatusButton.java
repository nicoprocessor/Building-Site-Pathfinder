package com.unibs.buildingsitepathfinder;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.View;
import android.widget.Button;

@SuppressLint("AppCompatCustomView")
public class CustomStatusButton extends Button implements View.OnClickListener {
    private boolean status;

    public CustomStatusButton(Context context) {
        super(context);
        this.status = true;
    }

    @Override
    public void onClick(View v) {

    }
}
