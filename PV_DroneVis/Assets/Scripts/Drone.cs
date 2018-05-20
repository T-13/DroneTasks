using UnityEngine;

public class Drone : MonoBehaviour {

    public DroneData data; // Initial data from JSON
    public float speed = 1.0f; // Trajectory segment time length (default one per second)

    int step = 0;
    float startTime = 0.0f;
    Vector3 segmentStart;
    Vector3 segmentEnd;

    // Use this for initialization
    void Start() {
        // Move to next trajectory segment every speed unit
        InvokeRepeating("UpdatePosition", 0.0f, speed);
    }

    // Update is called once per frame
    void Update() {
        // Disable UpdatePosition if we are on last trajectory segment
        if (step >= data.trajectoryFlight.Length - 1) {
            CancelInvoke("UpdatePosition");

            // Disable Update if we are at the end of movement
            if (Time.time - startTime >= speed) {
                enabled = false;
            }
        }

        // Move drone every frame through current segment
        transform.position = Vector3.Lerp(segmentStart, segmentEnd, Time.time - startTime); ;
    }

    // Sets up data for next trajectory segment
    void UpdatePosition() {
        step++;
        startTime = Time.time;

        // Setup next segment (from last to next step)
        segmentStart = data.trajectoryFlight[step - 1];
        segmentEnd = data.trajectoryFlight[step];
    }
}
