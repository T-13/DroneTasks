using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;

public class Spawner : MonoBehaviour {
    [Serializable]
    public class Data {
        public BeaconData[] beacons;
        public DroneData[] drones;
    }

    public string dataPath = "data.json";
    public GameObject beaconObject;
    public GameObject droneObject;
    public Material trajectoryMaterial;
    public Canvas canvas;
    public GameObject trajectoryDropdown;

    List<Drone> drones = new List<Drone>();

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

        for (int i = 0; i < data.drones.Length; i++) {
            DroneData drone = data.drones[i];

            GameObject objectDrone = Instantiate(droneObject, drone.position, Quaternion.identity);
            Drone compDrone = objectDrone.GetComponent<Drone>();
            drones.Add(compDrone);
            compDrone.data = drone;
            objectDrone.name = drone.name;

            //List<string> dropdownOptions = new List<string>();
            List<Dropdown.OptionData> dropdownOptions = new List<Dropdown.OptionData>();

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

                // Add to selection
                Texture2D dropTexture = new Texture2D(1, 1);
                dropTexture.SetPixel(0, 0, randColor);
                dropTexture.Apply();
                Sprite dropImage = Sprite.Create(dropTexture, new Rect(0, 0, dropTexture.width, dropTexture.height), new Vector2(0, 0));
                dropdownOptions.Add(new Dropdown.OptionData(trajectory.name, dropImage));
            }

            // Create Dropdown for Trajectories selection
            GameObject dropdown = Instantiate(trajectoryDropdown);
            dropdown.transform.SetParent(canvas.transform, false);

            // Set name and position
            RectTransform dropdownRectTransform = dropdown.GetComponent<RectTransform>();
            dropdownRectTransform.name = drone.name + " Trajectory Selection";
            dropdownRectTransform.anchoredPosition3D = new Vector3(0, -30 * i, 0); // Move below previous
            dropdown.GetComponentInChildren<Text>().text = drone.name + ":";

            // Set options and register value changed event
            Dropdown compDropdown = dropdown.GetComponent<Dropdown>();
            compDropdown.AddOptions(dropdownOptions);

            compDropdown.onValueChanged.AddListener(delegate {
                compDrone.TrajectoryChanged(compDropdown.value);
            });
        }
    }

    public void ResetDrones() {
        foreach (Drone drone in drones) {
            drone.Reset();
        }
    }
}
