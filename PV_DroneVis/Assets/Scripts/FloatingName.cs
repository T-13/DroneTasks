using UnityEngine;

public class FloatingName : MonoBehaviour {
    public float textSize = 15;

    Camera mainCamera;

    // Use this for initialization
    void Start() {
        // Set name
        GetComponent<TextMesh>().text = transform.parent.name;

        // Cache main camera (expensive accessor)
        mainCamera = Camera.main;
    }

    // Update is called once per frame
    void Update() {
        // Orient name towards the Main Camera (actually aways as it is inverted) and scale it with distance
        Vector3 textScreenSpace = mainCamera.WorldToScreenPoint(transform.position);
        Vector3 adjustedScreenSpace = new Vector3(textScreenSpace.x + textSize, textScreenSpace.y, textScreenSpace.z);
        Vector3 adjustedWorldSpace = mainCamera.ScreenToWorldPoint(adjustedScreenSpace);
        transform.localScale = Vector3.one * (transform.position - adjustedWorldSpace).magnitude;
        transform.rotation = mainCamera.transform.rotation;
    }
}
