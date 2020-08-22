package com.unibs.buildingsitepathfinder;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;

import java.util.HashMap;
import java.util.Set;

import static android.support.v4.app.ActivityCompat.startActivityForResult;

/**
 * This class provides some basic functionality to monitor the Bluetooth connection and send messages to the robot
 */
public class BluetoothConnection {
    private static final int REQUEST_ENABLE_BT = 0;

    private BluetoothAdapter btAdapter;
    private HashMap<BluetoothDevice, DeviceInfo> pairedDevices;

    BluetoothConnection() {
        this.btAdapter = BluetoothAdapter.getDefaultAdapter();
        this.pairedDevices = new HashMap<>();
    }

    /**
     * Checks if the device in use supports Bluetooth
     *
     * @return true if the Bluetooth antenna is available and functioning correctly, otherwise false
     */
    public boolean checkBluetoothAvailability() {
        return this.btAdapter == null;
    }

    /**
     * Checks if Bluetooth service is enabled
     *
     * @return true if Bluetooth is enabled, otherwise false
     */
    public boolean checkBluetoothEnabled() {
        return this.btAdapter.isEnabled();
    }

    /**
     * Asks the user the permission to activate the Bluetooth service
     *
     * @return true if the Bluetooth is enabled at the end of the interaction, otherwise false
     */
    public boolean requestBluetoothActivation() {
        if (!this.btAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
        return this.btAdapter.isEnabled();
    }

    /**
     * Update the list of Bluetooth paired devices
     */
    public void refreshPairedDevices() {
        Set<BluetoothDevice> pairedDevices = this.btAdapter.getBondedDevices();

        if (pairedDevices.size() > 0) {
            for (BluetoothDevice device : pairedDevices) {
                DeviceInfo info = new DeviceInfo(device.getName(), device.getAddress());
                this.pairedDevices.put(device, info);
            }
        }
    }

    //TODO ping robot
    public boolean pingRobot() {
        return true;
    }

    public boolean sendString() {
        return false;
    }


    // Getters and setters
    public BluetoothAdapter getBtAdapter() {
        return btAdapter;
    }

    public void setBtAdapter(BluetoothAdapter btAdapter) {
        this.btAdapter = btAdapter;
    }

    public HashMap<BluetoothDevice, DeviceInfo> getPairedDevices() {
        return pairedDevices;
    }

    public void setPairedDevices(HashMap<BluetoothDevice, DeviceInfo> pairedDevices) {
        this.pairedDevices = pairedDevices;
    }

}

class DeviceInfo {
    String name;
    String hardwareAddress;

    public DeviceInfo(String name, String address) {
        this.name = name;
        this.hardwareAddress = address;
    }

    // Getters and setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getHardwareAddress() {
        return hardwareAddress;
    }

    public void setHardwareAddress(String hardwareAddress) {
        this.hardwareAddress = hardwareAddress;
    }

}
