package com.unibs.buildingsitepathfinder;

import android.content.Context;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Connection {
    private final int connectionTimeout = 15 * 1000;
    private final int readConnectionTimeout = 10 * 1000;

    private URL serverURL;
    private Context activityContext;

    public Connection(URL serverURL, Context context) {
        this.serverURL = serverURL;
        this.activityContext = context;
    }




    /**
     * Converts an InputStream to a printable string
     *
     * @param is the InputStream coming from the connection
     * @return the stream converted to a printable string
     */
    private String convertStreamToString(InputStream is) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line = null;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }


    /**
     * Tests if the server is online and reachable.
     *
     * @return true if the server is reachable, false otherwise
     */
    public boolean pingServer() {
        String requestMethod = "GET";
        try {
            executeRequest(this.serverURL, requestMethod);
        } catch (Exception e) {
            return false;
        }
        return true;
    }

    /**
     * Executes a request online
     *
     * @param url the URL of the request
     * @throws Exception in case the host is unreachable or the connection expires while waiting for response
     */
    public String executeRequest(URL url, String requestMethod) throws Exception {
        HttpURLConnection conn = null;

        conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(this.readConnectionTimeout); //Milliseconds
        conn.setConnectTimeout(this.connectionTimeout); //Milliseconds
        conn.setRequestMethod("GET");
        conn.setDoInput(true);

        // Establish connection
        conn.connect();
        return convertStreamToString(conn.getInputStream());
    }
}
