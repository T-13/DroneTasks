using System;
using UnityEngine;

[Serializable]
public class DroneData {

    public string name;
    public Vector3 position;
    public Vector3[] trajectoryPlanned;
    public Vector3[] trajectoryFlight;
}
