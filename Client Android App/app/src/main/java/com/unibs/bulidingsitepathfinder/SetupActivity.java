package com.unibs.bulidingsitepathfinder;

import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

public class SetupActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {
    private final int maxHeight = 10;
    private final int maxWidth = 10;
    private final String DEBUG_TAG = "NetworkStatusExample";

    private Button network_btn;
    private Button findPath_btn;
    private Button reset_btn;
    private Button test_btn;
    private AlertDialog.Builder builder;

    //    private int selectedWidth, selectedHeight;
    Spinner heightSpinner, widthSpinner;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

//        LinearLayout lm = findViewById(R.id.linearMain);
//
//        //Layout parameters used to display buttons
//        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
//                LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
//
//        //Create four
//        for (int index = 0; index <= 4; index++) {
//            LinearLayout innerLayout = new LinearLayout(this);
//            innerLayout.setOrientation(LinearLayout.HORIZONTAL);
//
//            // Create Button
//            Button btn = new Button(this);
//            // Give button an ID
//            btn.setId(index + 1);
//            btn.setText("test");
//            btn.setLayoutParams(params);
//
//            final int indexBtn = index;
//            // Set click listener for button
//            btn.setOnClickListener(new View.OnClickListener() {
//                public void onClick(View v) {
//                    Toast.makeText(getApplicationContext(),
//                            "Clicked Button Index :" + indexBtn,
//                            Toast.LENGTH_SHORT).show();
//                }
//            });
//
//            //Add button to LinearLayout
//            innerLayout.addView(btn);
//            //Add button to LinearLayout defined in XML
//            lm.addView(innerLayout);
//        }

//         //Spinner element
//        heightSpinner = findViewById(R.id.heightSpinner);
//        heightSpinner.setOnItemSelectedListener(this);
//
//        widthSpinner = findViewById(R.id.widthSpinner);
//        widthSpinner.setOnItemSelectedListener(this);
//
//        ArrayList<String> availableHeights = new ArrayList<>();
//        ArrayList<String> availableWeights = new ArrayList<>();
//
//
//        for (int i = 2; i < maxHeight + 1; i++)
//            availableHeights.add(String.valueOf(i));
//
//        for (int i = 2; i < maxWidth + 1; i++)
//            availableWeights.add(String.valueOf(i));
//
//        // Creating adapter for spinner
//        ArrayAdapter<String> dataAdapterHeights = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, availableHeights);
//        ArrayAdapter<String> dataAdapterWidths = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, availableWeights);
//
//        // Drop down layout style - list view with radio button
//        dataAdapterHeights.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
//        dataAdapterWidths.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
//
//        // attaching data adapter to spinner
//        heightSpinner.setAdapter(dataAdapterHeights);
//        widthSpinner.setAdapter(dataAdapterWidths);

//        network_btn = this.findViewById(R.id.networkButton);
        findPath_btn = this.findViewById(R.id.findPathButton);
        reset_btn = this.findViewById(R.id.resetButton);
//        test_btn = this.findViewById(R.id.testDialogButton);


//        Log.d(DEBUG_TAG, "Wifi connected: " + isWifiConn);
//        Log.d(DEBUG_TAG, "Mobile connected: " + isMobileConn);
//        Log.d(DEBUG_TAG, "Bluetooth connected: " + isBTConn);

        // Next example

//        final TextView mTextView = (TextView) findViewById(R.id.text);
//
//        RequestQueue queue = Volley.newRequestQueue(this);
//        String url ="http://www.google.com";
//
//// Request a string response from the provided URL.
//        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
//                new Response.Listener<String>() {
//                    @Override
//                    public void onResponse(String response) {
//                        // Display the first 500 characters of the response string.
//                        mTextView.setText("Response is: "+ response.substring(0,500));
//                    }
//                }, new Response.ErrorListener() {
//            @Override
//            public void onErrorResponse(VolleyError error) {
//                mTextView.setText("That didn't work!");
//            }
//        });

// Add the request to the RequestQueue.
//        queue.add(stringRequest);
    }

    public void displayNetworkStatus(View v) {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo;

        boolean isWifiConn = false;
        boolean isBTConn = false;

        // just to satisfy the compiler
        if (connMgr != null) {
            Log.d(DEBUG_TAG, "Hello");
            networkInfo = connMgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI);
            isWifiConn = networkInfo.isConnected();
            networkInfo = connMgr.getNetworkInfo(ConnectivityManager.TYPE_BLUETOOTH);
            isBTConn = networkInfo.isConnected();
        }

        Toast.makeText(this.getApplicationContext(), "Wifi is connected: " + isWifiConn, Toast.LENGTH_SHORT).show();
        Toast.makeText(this.getApplicationContext(), "Bluetooth is connected: " + isBTConn, Toast.LENGTH_SHORT).show();
    }

    public void checkBluetoothConnection(View v) {
        final BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        if (!mBluetoothAdapter.isEnabled()) {
            Log.d("TEST DIALOG", "Hey there!");
            builder = new AlertDialog.Builder(this.getActivity());

            builder.setMessage(R.string.dialog_message);
            builder.setTitle(R.string.dialog_title);
            builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    mBluetoothAdapter.enable();

                }
            });
            builder.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // User cancelled the dialog
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();
        }
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        String selectedItem = parent.getSelectedItem().toString();
        Toast.makeText(this, selectedItem, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    public Context getActivity() {
        return this;
    }
}
