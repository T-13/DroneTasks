using UnityEngine;

public class Drone : MonoBehaviour {
    public DroneData data; // Initial data from JSON
    public float speed = 1.0f; // Flight data segment time length (default one per second)

    int step = 0;
    float startTime = 0.0f;
    Vector3 segmentStart;
    Vector3 segmentEnd;

    // Use this for initialization
    void Start() {
        // Move to next flight data segment every speed unit, disable if not enough points
        if (data.flightData.Length > 1) {
            InvokeRepeating("UpdatePosition", 0.0f, speed);
        } else {
            enabled = false;
        }
    }

    // Update is called once per frame
    void Update() {
        // Disable UpdatePosition if we are on last flight data segment
        if (step >= data.flightData.Length - 1) {
            CancelInvoke("UpdatePosition");

            // Disable Update if we are at the end of movement
            if (Time.time - startTime >= speed) {
                enabled = false;
            }
        }

        // Move drone every frame through current segment
        transform.position = Vector3.Lerp(segmentStart, segmentEnd, Time.time - startTime); ;
    }

    // Sets up data for next flight data segment
    void UpdatePosition() {
        step++;
        startTime = Time.time;

        // Setup next segment (from last to next step)
        segmentStart = data.flightData[step - 1];
        segmentEnd = data.flightData[step];
    }
}
