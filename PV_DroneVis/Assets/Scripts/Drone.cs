using UnityEngine;

public class Drone : MonoBehaviour {
    public DroneData data; // Initial data from JSON
    public float speed = 1.0f; // Flight data segment time length (default one per second)

    Trajectory currentTrajectory;
    int step;
    float startTime;
    Vector3 segmentStart;
    Vector3 segmentEnd;

    // Use this for initialization
    void Start() {
        currentTrajectory = data.trajectories[0];

        BeginTravel();
    }

    // Update is called once per frame
    void Update() {
        // Disable UpdatePosition if we are on last flight data segment
        if (step >= currentTrajectory.data.Length - 1) {
            CancelInvoke("UpdatePosition");

            // Disable Update if we are at the end of movement
            if (Time.time - startTime >= speed) {
                enabled = false;
            }
        }

        // Move drone every frame through current segment
        transform.position = Vector3.Lerp(segmentStart, segmentEnd, Time.time - startTime); ;
    }

    void BeginTravel() {
        // Move to next flight data segment every speed unit, disable if not enough points
        if (currentTrajectory.data.Length > 1) {
            step = 0;
            startTime = 0.0f;

            if (enabled) {
                CancelInvoke("UpdatePosition");
                enabled = false;
            }

            InvokeRepeating("UpdatePosition", 0.0f, speed);
            enabled = true;
        }
    }

    // Sets up data for next flight data segment
    void UpdatePosition() {
        step++;
        startTime = Time.time;

        // Setup next segment (from last to next step)
        segmentStart = currentTrajectory.data[step - 1];
        segmentEnd = currentTrajectory.data[step];
    }

    public void TrajectoryChanged(int trajectoryIndex) {
        currentTrajectory = data.trajectories[trajectoryIndex];
        BeginTravel();
    }

    public void Reset() {
        BeginTravel();
    }
}
