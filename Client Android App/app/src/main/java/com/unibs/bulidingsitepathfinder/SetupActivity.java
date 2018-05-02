package com.unibs.bulidingsitepathfinder;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.ArrayList;

public class SetupActivity extends Activity implements AdapterView.OnItemSelectedListener {
    private final int maxHeight = 10;
    private final int maxWidth = 10;
    private int selectedWidth, selectedHeight;
    private Spinner heightSpinner, widthSpinner;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

        // Spinner element
        heightSpinner = findViewById(R.id.heightSpinner);
        heightSpinner.setOnItemSelectedListener(this);

        widthSpinner = findViewById(R.id.widthSpinner);
        widthSpinner.setOnItemSelectedListener(this);

        ArrayList<String> availableHeights = new ArrayList<>();
        ArrayList<String> availableWeights = new ArrayList<>();


        for (int i = 2; i < maxHeight + 1; i++)
            availableHeights.add(String.valueOf(i));

        for (int i = 2; i < maxWidth + 1; i++)
            availableWeights.add(String.valueOf(i));

        // Creating adapter for spinner
        ArrayAdapter<String> dataAdapterHeights = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, availableHeights);
        ArrayAdapter<String> dataAdapterWidths = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, availableWeights);

        // Drop down layout style - list view with radio button
        dataAdapterHeights.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        dataAdapterWidths.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        // attaching data adapter to spinner
        heightSpinner.setAdapter(dataAdapterHeights);
        widthSpinner.setAdapter(dataAdapterWidths);
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        String selectedItem = parent.getSelectedItem().toString();
        Toast.makeText(this, selectedItem, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
}
