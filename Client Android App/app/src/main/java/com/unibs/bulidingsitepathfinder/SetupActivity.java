package com.unibs.bulidingsitepathfinder;

import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.support.constraint.ConstraintLayout;
import android.support.constraint.ConstraintSet;
import android.support.constraint.Guideline;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.w3c.dom.Text;

import java.util.ArrayList;

public class SetupActivity extends AppCompatActivity {
    private final int maxRows = 10;
    private final int maxCols = 10;
    private final int default_size = 5;

    private int selectedCols, selectedRows;
    private boolean isBTConnected, isServerConnected;

    private Button findPathBtn, refreshBtn;
    private TextView obstaclesCount, freeSpotsCount, robotPosition, targetPosition;
    private AlertDialog.Builder builder;
    private ConstraintLayout grid;
    private ImageView rowsIcon, colsIcon;
    private Spinner rowSpinner, colSpinner;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);
        getWindow().getDecorView().setBackgroundColor(Color.WHITE);

        // Layout components init
        findPathBtn = this.findViewById(R.id.findPathButton);
        refreshBtn = this.findViewById(R.id.resetButton);

        obstaclesCount = this.findViewById(R.id.obstaclesCountTextView);
        freeSpotsCount = this.findViewById(R.id.freeSpotsTextView);
        robotPosition = this.findViewById(R.id.robotPositionTextView);
        targetPosition = this.findViewById(R.id.targetPositionTextView);

        rowSpinner = findViewById(R.id.rowSpinner);
        colSpinner = findViewById(R.id.colSpinner);

        grid = findViewById(R.id.gridConstraintLayout);
        grid.setBackgroundColor(Color.CYAN);

        ArrayList<ArrayList<TextView>> gridButtons = new ArrayList<>();
        ArrayList<TextView> currentRow = new ArrayList<>();
        ConstraintSet constraints = new ConstraintSet();

        int rows = 3;
        int cols = 3;

        if (cols > 3 || rows > 3) {
            // Add new buttons to the chains
        }

        int[] chainIds = new int[rows * cols];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                TextView tv = new TextView(this.getApplicationContext());
                int viewIndex = c + c * r;
                tv.setText(String.valueOf(viewIndex));
                tv.setId(viewIndex);
                tv.setOnClickListener(new View.OnClickListener() {
                                          @Override
                                          public void onClick(View v) {
                                              Log.d("Text View pressed", String.valueOf(tv.getId()));
                                          }
                                      }
                );
                tv.setLayoutParams(new ConstraintLayout.LayoutParams(
                        ConstraintLayout.LayoutParams.WRAP_CONTENT,
                        ConstraintLayout.LayoutParams.WRAP_CONTENT
                ));
                tv.setClickable(true);
                tv.setBackgroundResource(R.drawable.rounded_corner);
                tv.setTextColor(R.color.colorPrimary);
                tv.setMinWidth(120);
                tv.setElevation(10);
                tv.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                tv.setPadding(10, 10, 10, 10);

                chainIds[viewIndex] = tv.getId();
//                grid.addView(tv, viewIndex);
                currentRow.add(tv);
            }
        }

//
//        constraints.clone(grid);

//        constraints.connect(
//                currentrow.get(0).getid(), constraintlayout.layoutparams.left,
//                grid.getid(), constraintlayout.layoutparams.left, 16);
//
//        constraints.connect(
//                currentrow.get(0).getid(), constraintlayout.layoutparams.top,
//                grid.getid(), constraintlayout.layoutparams.top);
//
//        constraints.applyto(grid);
//
//        constraints.connect(
//                currentrow.get(0).getid(), constraintlayout.layoutparams.bottom,
//                currentrow.get(1).getid(), constraintlayout.layoutparams.bottom);
//
//        constraints.connect(
//                1, constraintlayout.layoutparams.left,
//                grid.getid(), constraintlayout.layoutparams.right, 16);
//
//        constraints.connect(
//                currentRow.get(1).getId(), ConstraintLayout.LayoutParams.TOP,
//                currentRow.get(0).getId(), ConstraintLayout.LayoutParams.TOP, 16);

//        Log.d("Testing Responsive Layout", "id tv1: " + String.valueOf(currentRow.get(0).getId()));
//        Log.d("Testing Responsive Layout", "id tv2: " + String.valueOf(currentRow.get(1).getId()));
//        Log.d("Testing Responsive Layout", "id grid: " + String.valueOf(grid.getId()));


//        constraints.applyTo(grid);

//        ConstraintSet constraints = new ConstraintSet();
//        constraints.clone(grid);


//        constraints.createHorizontalChain(grid.getId(), ConstraintSet.LEFT, grid.getId(), ConstraintSet.RIGHT,
//                chainIds, null, ConstraintSet.CHAIN_PACKED);


//        constraints.applyTo(grid);

//        int btnCols = 1;
//        int btnRows = 3;
//
//        int[] chainIds = new int[btnCols * btnRows];
//        ArrayList<Button> rowBtns = new ArrayList<>();
//
//        for (int c = 0; c < btnCols; c++) {
//            for (int r = 0; r < btnRows; r++) {
//                Button btn = new Button(this.getActivity().getApplicationContext());
//                int btnIndex = r + c * r;
//                btn.setId(btnIndex);
//                btn.setText(String.valueOf(btnIndex));
//                btn.setLayoutParams(new ConstraintLayout.LayoutParams(
//                        150,
//                        ConstraintLayout.LayoutParams.WRAP_CONTENT));
//
//                chainIds[btnIndex] = btn.getId();
//                grid.addView(btn, btnIndex);
//                rowBtns.add(btn);
//            }
//        }
//
//        constraints.clone(grid);
//
//        constraints.createHorizontalChain(
//                rowBtns.get(0).getId(), ConstraintSet.LEFT,
//                rowBtns.get(rowBtns.size() - 1).getId(), ConstraintSet.RIGHT,
//                chainIds, null, ConstraintSet.CHAIN_SPREAD);


//        Display display = getWindowManager().getDefaultDisplay();
//        Point size = new Point();
//        display.getSize(size);
//        int displayWidth = size.x;
//        int displayHeight = size.y;

//        updateGrid(3, 1);

        // Attaching listeners to spinners
        rowSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {

            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                rowSpinner.setSelection(Integer.parseInt(parent.getSelectedItem().toString()) - 3);
//                Toast.makeText(getApplicationContext(), parent.getItemAtPosition(pos).toString(), Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                rowSpinner.setSelection(R.string.default_size);
            }
        });

        colSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {

            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                colSpinner.setSelection(Integer.parseInt(parent.getSelectedItem().toString()) - 3);
//                Toast.makeText(getApplicationContext(), parent.getItemAtPosition(pos).toString(), Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                colSpinner.setSelection(R.string.default_size);
            }
        });


        // onCreate routine
//        isServerConnected = checkWiFiEnabled();
//
//        if (!isServerConnected)
//            askEnableWifi();


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

    /**
     * Checks if the Bluetooth is enabled and connected
     *
     * @return true if Bluetooth module is connected, else false
     */
    public boolean checkBluetoothEnabled() {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return connMgr != null && connMgr.getNetworkInfo(ConnectivityManager.TYPE_BLUETOOTH).isConnected();
    }

    /**
     * Checks if the WiFi is enabled
     *
     * @return true if WiFi module is enabled, else false
     */
    public boolean checkWiFiEnabled() {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return connMgr != null && connMgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnected();
    }

    /**
     * Ask the user to enable automatically the Wifi
     */
    public void askEnableWifi() {
        final WifiManager wifiManager = (WifiManager) this.getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        if (!checkWiFiEnabled()) {
            // Create an AlertDialog in order to ask to the user to enable automatically the WiFi module
            builder = new AlertDialog.Builder(this.getActivity());

            builder.setMessage(R.string.dialog_message_WiFi);
            builder.setTitle(R.string.dialog_title_WiFi);

            builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    if (wifiManager != null) {
                        wifiManager.setWifiEnabled(true);
                        Toast.makeText(SetupActivity.this.getApplicationContext(), "Done!", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(SetupActivity.this.getApplicationContext(), "Oops!", Toast.LENGTH_SHORT).show();
                    }
                }
            });

            builder.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // Do nothing
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();
        }
    }

    /**
     * Ask the user to enable automatically the Bluetooth module
     */
    public void askEnableBluetooth() {
        final BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        if (!checkBluetoothEnabled()) {
            // Create an AlertDialog in order to ask to the user to enable automatically the BT module
            builder = new AlertDialog.Builder(this.getActivity());

            builder.setMessage(R.string.dialog_message_BT);
            builder.setTitle(R.string.dialog_title_BT);

            builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    mBluetoothAdapter.enable();
                    Toast.makeText(SetupActivity.this.getApplicationContext(), "Done!", Toast.LENGTH_SHORT).show();
                }
            });

            builder.setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    // Do nothing
                }
            });

            AlertDialog dialog = builder.create();
            dialog.show();
        }
    }


    /**
     * Send the current instance of the maze to the server if everything is connected.
     * This method is linked to the onClick action of the findPath button.
     *
     * @param view findPath button
     */
    public void sendInstance(View view) {
        //TODO
    }

    /**
     * Resets the site configuration to the default settings.
     * This method is linked to the onClick action of the reset button
     *
     * @param v reset button
     */
    public void resetGrid(View v) {
        //TODO
    }

    public Context getActivity() {
        return this;
    }
}


