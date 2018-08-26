package com.unibs.buildingsitepathfinder;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.graphics.Point;
import android.net.ConnectivityManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.support.constraint.ConstraintLayout;
import android.support.constraint.ConstraintSet;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.util.ArrayList;

public class SetupActivity extends AppCompatActivity {
    private final int maxRows = 9;
    private final int maxCols = 9;
    private final int default_size = 5;

    private int selectedCols, selectedRows;
    private boolean isBTConnected, isServerConnected;
    private ArrayList<CustomButton> gridButtons;
    private String startingOrientation;

    //Visual components
    private Button findPathBtn, resetBtn;
    private TextView obstaclesCounter, freeSpotsCount, startPosition, targetPosition;
    private AlertDialog.Builder builder;
    private ConstraintLayout grid;
    private GridManager gridManager;
    private ImageView rowsIcon, colsIcon;
    private Spinner rowSpinner, colSpinner;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);
        getWindow().getDecorView().setBackgroundColor(Color.WHITE);

        // Layout components init
        findPathBtn = this.findViewById(R.id.findPathButton);
        resetBtn = this.findViewById(R.id.resetButton);
        obstaclesCounter = this.findViewById(R.id.obstaclesCountTextView);
        startPosition = this.findViewById(R.id.robotPositionTextView);
        targetPosition = this.findViewById(R.id.targetPositionTextView);

        colSpinner = findViewById(R.id.colSpinner);
        colSpinner.setSelection(default_size - 2);

        grid = findViewById(R.id.gridConstraintLayout);

        ConstraintSet constraints = repaintGrid(default_size, default_size, grid, gridManager);
        constraints.applyTo(grid);

        this.gridManager = new GridManager(gridButtons, grid, default_size, obstaclesCounter, startPosition, targetPosition);

        //Implementing listeners
        colSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {

            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                colSpinner.setSelection(Integer.parseInt(parent.getSelectedItem().toString()) - 3);
                resetBtn.performClick();
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                colSpinner.setSelection(R.string.default_size);
            }
        });

        resetBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int size = Integer.parseInt(colSpinner.getSelectedItem().toString());

                grid.removeAllViews();

                ConstraintSet constraints = repaintGrid(size, size, grid, gridManager);
                constraints.applyTo(grid);

                SetupActivity.this.gridManager = resetGridManager(size);
            }
        });

        findPathBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String maze = SetupActivity.this.gridManager.convertToMazeMap();

                if (maze.length() == 0) {
                    //Ask the user to provide both start and end of the maze
                    askUserToFixMazeDialog();

                } else { //the maze is correct
                    //Ask user to select the starting orientation
                    askStartingOrientationDialog();

                    //Check server connection - first check if wifi and data are enabled - if false, ask the user to enable it

                    //If the server is connected send request String via Volley

                    //If the response is positive then send the plan to the robot -> new activity
                }
            }
        });
    }


    /**
     * Rebuilds the grid at its default state, with the given dimension, and returns the
     * ConstraintSet that has to be applied to the external container (Constraint Layout).
     *
     * @param rows the rows of the grid
     * @param cols the columns of the grid
     * @param grid the layout that is going to wrap the entire grid
     */
    public ConstraintSet repaintGrid(int rows, int cols, ConstraintLayout grid, GridManager
            gridManager) {
        ArrayList<CustomButton> gridButtons = new ArrayList<CustomButton>();
        ConstraintSet constraints = new ConstraintSet();

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);

        int screenWidth = dm.widthPixels;
        int screenHeight = dm.heightPixels;
        double marginToWidthRatio = 23.0 / 85.0;

        int btnWidth = (int) ((screenWidth - 66) / (marginToWidthRatio * cols + marginToWidthRatio + cols));
        int btnHeight = btnWidth;

        int[] chainIds = new int[rows * cols];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                CustomButton cb = new CustomButton(this.getApplicationContext(), gridManager);

                int viewIndex = c + r * cols;
                cb.setCoordinates(new Point(r, c));
                cb.setId(viewIndex);
                cb.setWidth(btnWidth);
                cb.setHeight(btnHeight);
                cb.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);

                chainIds[viewIndex] = cb.getId();
                gridButtons.add(cb);
                grid.addView(cb, viewIndex);
            }
        }

        constraints.clone(grid);

        int verticalMargin = (int) (btnWidth * marginToWidthRatio);
        int horizontalMargin = verticalMargin;

        for (int currentId = 0; currentId < cols * rows; currentId++) {
            constraints.connect(
                    grid.getViewById(currentId).getId(), ConstraintLayout.LayoutParams.TOP,
                    grid.getId(), ConstraintLayout.LayoutParams.TOP,
                    verticalMargin * ((int) Math.floor((currentId / cols)) + 1) + btnHeight * ((int) Math.floor((currentId / cols))));

            constraints.connect(
                    grid.getViewById(currentId).getId(), ConstraintLayout.LayoutParams.LEFT,
                    grid.getId(), ConstraintLayout.LayoutParams.LEFT,
                    horizontalMargin * ((currentId % cols) + 1) + btnWidth * (currentId % cols));
        }

        //Update GridManager references
        this.gridButtons = gridButtons;
        return constraints;
    }

    /**
     * Rebuilds the grid manager
     *
     * @return
     */
    public GridManager resetGridManager(int size) {
        return new GridManager(this.gridButtons, this.grid, size, this.obstaclesCounter,
                this.startPosition, this.targetPosition);
    }

    /**
     * Asks user to select the starting orientation of the robot
     */
    public void askStartingOrientationDialog() {
        builder = new AlertDialog.Builder(SetupActivity.this);
        builder.setTitle(R.string.dialog_title_starting_orientation)
                .setSingleChoiceItems(R.array.orientations, 0,
                        new DialogInterface.OnClickListener() {

                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                ListView lw = ((AlertDialog) dialog).getListView();
                                SetupActivity.this.setStartingOrientation((String) lw.getAdapter().getItem(lw.getCheckedItemPosition()));
                            }
                        })
                .setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        try {
                            SetupActivity.this.gridManager.displayStartingOrientation(
                                    SetupActivity.this.getStartingOrientation(),
                                    SetupActivity.this.gridManager.getStartButton().getId());
                            Log.d("arrows", String.valueOf(SetupActivity.this.gridManager.getStartButton().getId()));

                            Toast.makeText(SetupActivity.this.getApplicationContext(),
                                    "Setup completed!", Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            Toast.makeText(SetupActivity.this.getApplicationContext(),
                                    "Please select a direction!", Toast.LENGTH_SHORT).show();
                        }
                    }
                })
                .setNegativeButton(R.string.cancel, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        Toast.makeText(SetupActivity.this.getApplicationContext(),
                                "Canceled!", Toast.LENGTH_SHORT).show();
                    }
                });

        AlertDialog dialog = builder.create();
        dialog.show();
    }

    /**
     * Informs the user that the maze is missing some required cells.
     */
    public void askUserToFixMazeDialog() {
        builder = new AlertDialog.Builder(SetupActivity.this);

        builder.setMessage(R.string.dialog_message_missing_required_cell);
        builder.setTitle(R.string.dialog_title_missing_required_cell);

        builder.setPositiveButton(R.string.understand, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                //Do nothing and close dialog
            }
        });

        AlertDialog dialog = builder.create();
        dialog.show();
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
    public void askEnableWifiDialog() {
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
    public void askEnableBluetoothDialog() {
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

    //Getters and Setters
    public Context getActivity() {
        return this;
    }

    public GridManager getGridManager() {
        return gridManager;
    }

    public String getStartingOrientation() {
        return startingOrientation;
    }

    public void setStartingOrientation(String startingOrientation) {
        this.startingOrientation = startingOrientation;
    }

    public void setGridManager(GridManager gridManager) {
        this.gridManager = gridManager;
    }
}



