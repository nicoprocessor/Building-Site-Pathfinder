package com.unibs.buildingsitepathfinder;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.content.Context;
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
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class SetupActivity extends AppCompatActivity {
    //    private final int maxRows = 9;
//    private final int maxCols = 9;
    private final int defaultSize = 5;
    private final String defaultStartingOrientation = "North";
    private final String serverURL = "https://flask-maze-solver.herokuapp.com/";

    private ArrayList<CustomGridCellButton> gridButtons;
    private String startingOrientation;
    private ServerConnection serverConnection;
    private String mazeInstance;
    private String mazeSolution;

    //Visual components
    private Button findPathBtn, resetBtn, pingBtn;
    private TextView obstaclesCounter, startPosition, targetPosition;
    private AlertDialog.Builder builder;
    private ConstraintLayout grid;
    private GridManager gridManager;
    private Spinner colSpinner;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);
        getWindow().getDecorView().setBackgroundColor(Color.WHITE);

        // Init serverConnection
        serverConnection = new ServerConnection(serverURL, this.getApplicationContext(), this);

        // Layout components init
        findPathBtn = this.findViewById(R.id.findPathButton);
        resetBtn = this.findViewById(R.id.resetButton);
        pingBtn = this.findViewById(R.id.pingButton);
        obstaclesCounter = this.findViewById(R.id.obstaclesCountTextView);
        startPosition = this.findViewById(R.id.robotPositionTextView);
        targetPosition = this.findViewById(R.id.targetPositionTextView);

        colSpinner = findViewById(R.id.colSpinner);
        colSpinner.setSelection(defaultSize - 2);

        grid = findViewById(R.id.gridConstraintLayout);

        //Ask the user to enable WiFi and Bluetooth
        if (!isBluetoothEnabled() || !isWiFiEnabled()) {
            askEnableConnectivityDialog(isWiFiEnabled(), isBluetoothEnabled());
        }

        // Building the grid
        ConstraintSet constraints = repaintGrid(defaultSize, defaultSize, grid, gridManager);
        constraints.applyTo(grid);
        this.startingOrientation = defaultStartingOrientation;
        this.gridManager = new GridManager(gridButtons, grid, defaultSize, obstaclesCounter, startPosition, targetPosition);

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


        // Send ping to the server
        pingBtn.setOnClickListener(v -> {
            if (pingServer())
                Toast.makeText(this.getApplicationContext(),
                        "The server is online!", Toast.LENGTH_SHORT).show();
            else
                Toast.makeText(this.getApplicationContext(),
                        "Server unreachable!", Toast.LENGTH_SHORT).show();
        });


        // Reset maze instance
        resetBtn.setOnClickListener(v -> {
            int size = Integer.parseInt(colSpinner.getSelectedItem().toString());
            grid.removeAllViews();

            //Reset view
            ConstraintSet constraints1 = repaintGrid(size, size, grid, gridManager);
            constraints1.applyTo(grid);

            //Reset gridManager with the new grid buttons
            SetupActivity.this.gridManager = resetGridManager(size);

            //
            constraints1 = repaintGrid(size, size, grid, gridManager);
            constraints1.applyTo(grid);
        });


        // Find maze solution
        findPathBtn.setOnClickListener(v -> {
            String mazeInstance = SetupActivity.this.gridManager.convertToMazeMap();

            if (mazeInstance.length() == 0) {
                askUserToFixMazeDialog();
            } else {
                SetupActivity.this.setMazeInstance(mazeInstance);
                startMazeSolutionRoutineDialog();
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
        ArrayList<CustomGridCellButton> gridButtons = new ArrayList<CustomGridCellButton>();
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
                CustomGridCellButton cb = new CustomGridCellButton(this.getApplicationContext(), gridManager);

                int viewIndex = c + r * cols;
                cb.setCoordinates(new Point(r, c));
                cb.setId(viewIndex);
                cb.setWidth(btnWidth);
                cb.setHeight(btnHeight);
//                cb.setText(String.valueOf(viewIndex));
                cb.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);

                cb.setStatus("Empty");

                chainIds[viewIndex] = cb.getId();
                gridButtons.add(cb);
                grid.addView(cb, viewIndex);
            }
        }

        //Building the actual grid
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
     * @return the rebuilt grid manager
     */
    private GridManager resetGridManager(int size) {
        this.mazeInstance = "";

        return new GridManager(this.gridButtons, this.grid, size, this.obstaclesCounter,
                this.startPosition, this.targetPosition);
    }

    /**
     * Send the current instance of the maze to the server if everything is connected.
     */
    private void sendMazeInstance() {
        this.serverConnection.sendMazeInstance(
                String.valueOf(this.startingOrientation.charAt(0)),
                this.mazeInstance);
    }


    /**
     * Update the solution when the server is ready
     *
     * @param mazeSolution the computed maze solution
     */
    public void updateSolutionFromCallback(String mazeSolution) {
        this.mazeSolution = extractSolutionPlanFromJSON(mazeSolution);


        Log.d("Bingo", this.mazeSolution);
//        Log.d("Bingo", "Starting orientation: " + this.startingOrientation);

        if (this.mazeSolution.length() > 0) {
            if (this.mazeSolution.length() == 1) { //Impossible maze
                Toast.makeText(this.getApplicationContext(), "Impossible maze!", Toast.LENGTH_SHORT).show();
            } else { // plan found
                Toast.makeText(this.getApplicationContext(), "Solution found: " + this.mazeSolution, Toast.LENGTH_SHORT).show();
                SetupActivity.this.gridManager.solutionToGridButtons(this.mazeSolution, this.getStartingOrientation());
            }
        }
    }


    /**
     * Asks user to select the starting orientation of the robot and sends the instance to the server
     */
        private void startMazeSolutionRoutineDialog() {
        builder = new AlertDialog.Builder(SetupActivity.this);

        builder.setTitle(R.string.dialog_title_starting_orientation)
                .setSingleChoiceItems(R.array.orientations, 0,
                        (dialog, which) -> {
                            ListView lw = ((AlertDialog) dialog).getListView();
                            SetupActivity.this.setStartingOrientation((String) lw.getAdapter().getItem(lw.getCheckedItemPosition()));
                        })
                .setPositiveButton(R.string.solve_maze, (dialog, id) -> {
//                    try {
                    SetupActivity.this.gridManager.displayStartingOrientation(
                            SetupActivity.this.getStartingOrientation(),
                            SetupActivity.this.gridManager.getStartButton().getId());

                    Toast.makeText(SetupActivity.this.getApplicationContext(),
                            "Sending request to server...", Toast.LENGTH_SHORT).show();

                    // Solve maze
                    sendMazeInstance();
                });

        AlertDialog dialog = builder.create();
        dialog.show();
    }

    /**
     * Informs the user that the maze is missing some required cells.
     */
    private void askUserToFixMazeDialog() {
        builder = new AlertDialog.Builder(SetupActivity.this);

        builder.setMessage(R.string.dialog_message_missing_required_cell);
        builder.setTitle(R.string.dialog_title_missing_required_cell);

        builder.setPositiveButton(R.string.understand, (dialog, id) -> {
            //Do nothing and close dialog
        });

        AlertDialog dialog = builder.create();
        dialog.show();
    }

    /**
     * Pings the maze solver server
     *
     * @return true if the server is online and reachable
     */
    private boolean pingServer() {
        return serverConnection.pingServer();
    }

    /**
     * Check Bluetooth serverConnection with the robot
     *
     * @return true if the robot is reachable, false otherwise
     */
    private boolean pingRobot() {
        //TODO
        return false;
    }


    /**
     * Checks if the Bluetooth is enabled and connected
     *
     * @return true if Bluetooth module is connected, else false
     */
    private boolean isBluetoothEnabled() {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return connMgr != null && connMgr.getNetworkInfo(ConnectivityManager.TYPE_BLUETOOTH).isConnected();
    }

    /**
     * Checks if the WiFi is enabled
     *
     * @return true if WiFi module is enabled, else false
     */
    private boolean isWiFiEnabled() {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        return connMgr != null && connMgr.getNetworkInfo(ConnectivityManager.TYPE_WIFI).isConnected();
    }


    /**
     * Ask the user to enable WiFi and Bluetooth module automatically.
     */
    private void askEnableConnectivityDialog(boolean isWiFiEnabled, boolean isBluetoothEnabled) {
        final WifiManager wifiManager = (WifiManager) this.getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        final BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        builder = new AlertDialog.Builder(this.getActivity());
        builder.setMessage(R.string.dialog_message_enable_connectivity);
        builder.setTitle(R.string.dialog_title_enable_connectivity);

        builder.setPositiveButton(R.string.ok, (dialog, id) -> {
            if (!isWiFiEnabled) {
                if (wifiManager != null) {
                    wifiManager.setWifiEnabled(true);
                    Toast.makeText(SetupActivity.this.getApplicationContext(), "Done!", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(SetupActivity.this.getApplicationContext(), "WiFi not enabled!", Toast.LENGTH_SHORT).show();
                }
            }

            if (!isBluetoothEnabled) {
                mBluetoothAdapter.enable();
                Toast.makeText(SetupActivity.this.getApplicationContext(), "Done!", Toast.LENGTH_SHORT).show();
            }
        });

        builder.setNegativeButton(R.string.cancel, (dialog, id) -> {
            // Do nothing
        });

        AlertDialog dialog = builder.create();
        dialog.show();
    }


    /**
     * Extracts the string containing the computed plan from the JSON response
     *
     * @param json the server response in JSON format
     * @return the string containing the computed plan
     */
    private String extractSolutionPlanFromJSON(String json) {
        //String cleanup
        if (json.length() != 0) {
            json = json.replaceAll("\n", "");
            json = json.replaceAll(": ", "");
            json = json.replaceAll("\\}", "");
            json = json.replaceAll("\"", "");
            json = json.trim();

            StringBuilder sb = new StringBuilder();

            if (json.lastIndexOf("moves") == -1)
                return "";
            else {
                for (int i = json.lastIndexOf("moves"); i < json.length(); i++) {
                    if (!Character.isLetter(json.charAt(i)))
                        sb.append(json.charAt(i));

                    if (json.charAt(i) == ',')
                        break;
                }
            }
            return sb.toString();
        }
        return "";
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

    public String getMazeInstance() {
        return mazeInstance;
    }

    public void setMazeInstance(String mazeInstance) {
        this.mazeInstance = mazeInstance;
    }
}



