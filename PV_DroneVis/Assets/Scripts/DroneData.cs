using System;
using UnityEngine;

[Serializable]
public class DroneData {
    public string name;
    public Vector3 position;
    public Vector3[] flightData;
    public Vector3[] flightPlan;
}
