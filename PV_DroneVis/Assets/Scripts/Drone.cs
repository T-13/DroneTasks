using UnityEngine;

public class Drone : MonoBehaviour {

    public DroneData data; // Initial data from JSON

    private int step = 0;
    private LineRenderer trajectoryFlight;

    // Use this for initialization
    void Start() {
        trajectoryFlight = transform.Find("TrajectoryActual").GetComponent<LineRenderer>();
        trajectoryFlight.positionCount = data.trajectoryFlight.Length;
    }

    // Update is called once per frame
    void Update() {
        if (step >= data.trajectoryFlight.Length - 1) {
            enabled = false;
        }

        // TODO Only run every X time (eg. once per second)
        // TODO Move drone every step through Flight Trajectory

        // Draw Flight Trajectory
        trajectoryFlight.SetPosition(step, data.trajectoryFlight[step]);
        step++;
    }
}
