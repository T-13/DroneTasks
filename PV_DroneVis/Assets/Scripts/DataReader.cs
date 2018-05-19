using System;
using System.IO;
using UnityEngine;

public class DataReader : MonoBehaviour {

    [Serializable]
    public class Data {
        public BeaconData[] beacons;
        public DroneData[] drones;
    }

    public string dataPath = "data.json";
    public GameObject beaconObject;
    public GameObject droneObject;

    // Use this for initialization
    void Awake() {
        // Read JSON data from file
        StreamReader reader = new StreamReader(dataPath);
        string json = reader.ReadToEnd();
        reader.Close();

        Data data = JsonUtility.FromJson<Data>(json);

        // Spawn Beacons and Drones, set data and floating names
        foreach (BeaconData beacon in data.beacons) {
            GameObject objectBeacon = Instantiate(beaconObject, beacon.position, Quaternion.identity);
            objectBeacon.GetComponent<Beacon>().data = beacon;

            objectBeacon.transform.Find("FloatingName").GetComponent<TextMesh>().text = beacon.name;
        }

        foreach (DroneData drone in data.drones) {
            GameObject objectDrone = Instantiate(droneObject, drone.position, Quaternion.identity);
            objectDrone.GetComponent<Drone>().data = drone;

            objectDrone.transform.Find("FloatingName").GetComponent<TextMesh>().text = drone.name;
        }

        // TODO Draw Trajectory Planned
    }
}
