using System;
using UnityEngine;

[Serializable]
public class DroneData {
    public string name;
    public Vector3 position;
    public Trajectory[] trajectories;
}
