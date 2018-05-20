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
    public Material trajectoryMaterial;

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
            objectBeacon.name = beacon.name;
        }

        foreach (DroneData drone in data.drones) {
            GameObject objectDrone = Instantiate(droneObject, drone.position, Quaternion.identity);
            objectDrone.GetComponent<Drone>().data = drone;
            objectDrone.name = drone.name;

            // Draw Trajectories
            foreach (Trajectory trajectory in drone.trajectories) {
                // Create subobject
                GameObject objectTrajectory = new GameObject();
                objectTrajectory.transform.SetParent(objectDrone.transform);

                // Add Line component
                LineRenderer lineTrajectory = objectTrajectory.AddComponent<LineRenderer>();
                lineTrajectory.material = trajectoryMaterial;
                lineTrajectory.widthMultiplier = 0.05f;

                // Generate random color of line, set start and end to it
                Color randColor = new Color(UnityEngine.Random.value, UnityEngine.Random.value, UnityEngine.Random.value);
                lineTrajectory.startColor = randColor;
                lineTrajectory.endColor = randColor;

                // Set name and positions
                lineTrajectory.name = trajectory.name;
                lineTrajectory.positionCount = trajectory.data.Length;
                lineTrajectory.SetPositions(trajectory.data);
            }
        }
    }
}
