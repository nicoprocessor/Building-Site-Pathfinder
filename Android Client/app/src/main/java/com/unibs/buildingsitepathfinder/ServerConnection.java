package com.unibs.buildingsitepathfinder;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

/**
 * This class wraps some general methods to execute HTTP requests on the server.
 */
public class ServerConnection {
    private final String[] mazeSolutionParams = {"starting_orientation", "maze"};
    private final String[] pingParams = {"ping"};
    private final String emptyResponsePlaceHolder = "Empty Response";

    private String serverURL;
    private Context activityContext;
    private String response;
    private SetupActivity parentActivity;

    ServerConnection(String serverURL, Context context, SetupActivity parentActivity) {
        this.serverURL = serverURL;
        this.activityContext = context;
        this.response = emptyResponsePlaceHolder;
        this.parentActivity = parentActivity;
    }

    /**
     * Tests if the server is online and reachable.
     *
     * @return true if the server is reachable, false otherwise
     */
    boolean pingServer() {
        try {
            executeGETRequest("ping");
        } catch (Exception e) {
            Log.d("Error", "No ping");
            return false;
        }
        return true;
    }

    /**
     * Sends the maze instance to the server.
     * @param startingOrientation the starting orientation of the robot
     * @param maze the maze itself, converted to an ASCII string
     */
    void sendMazeInstance(String startingOrientation, String maze) {
        Log.d("Request params", "maze: " + maze +
                "\norientation: " + startingOrientation);
        executeGETRequest(startingOrientation, maze);
    }

    /**
     * Executes a GET request using Volley and sets the response
     * parameter with the actual response from the server.
     */
    private void executeGETRequest(String... requestParams) {
        RequestQueue queue = Volley.newRequestQueue(this.activityContext);
        String url = buildRequest(requestParams);

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                response -> {
//                    Log.d("Bingo params", response);

                    ServerConnection.this.parentActivity.updateSolutionFromCallback(response);
                }, error -> Log.d("Volley", "ServerConnection error"));

        queue.add(stringRequest);
    }

    /**
     * Build URL request
     *
     * @param requestParams the parameters of the request
     * @return the request in HTTP format
     */
    private String buildRequest(String... requestParams) {
        StringBuilder sb = new StringBuilder(this.getServerURL());
        sb.append("?");

        int paramCounter = 0;

        if (requestParams.length > 1) { //solve maze
            for (String s : requestParams) {
                s = s.replaceAll(" ", "");

                sb.append(mazeSolutionParams[paramCounter]);
                sb.append("=");
                sb.append(s);
                sb.append("&");
                paramCounter++;
            }
        } else {
            for (String s : requestParams) {
                s = s.replaceAll(" ", "");

                sb.append(pingParams[paramCounter]);
                sb.append("=");
                sb.append(s);
                sb.append("&");
            }
        }

//        Log.d("Request", "Sending request params: " + sb.toString());
        return sb.toString();
    }

    //Getters and setters

    public String getServerURL() {
        return serverURL;
    }

    public void setServerURL(String serverURL) {
        this.serverURL = serverURL;
    }

    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        Log.d("Setting response", "HELLO");
        this.response = response;
    }

}
