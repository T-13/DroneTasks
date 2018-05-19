using UnityEngine;

public class Drone : MonoBehaviour {

    public DroneData data; // Initial data from JSON

    private int step = 0;
    private LineRenderer trajectoryFlight;

    // Use this for initialization
    void Start() {
        // Find Flight Trajectory renderer
        trajectoryFlight = transform.Find("TrajectoryFlight").GetComponent<LineRenderer>();
    }

    // Update is called once per frame
    void Update() {
        if (step >= data.trajectoryFlight.Length - 1) {
            enabled = false;
        }

        // TODO Only run every X time (eg. once per second)
        // TODO Move drone every step through Flight Trajectory

        // Draw Flight Trajectory (increase vertex count and set position of current step)
        trajectoryFlight.positionCount++;
        trajectoryFlight.SetPosition(step, data.trajectoryFlight[step]);
        step++;
    }
}
