using UnityEngine;

public class CameraController : MonoBehaviour {

    static float movementSpeed = 1.0f;

    // Update is called once per frame
    void Update() {
        movementSpeed = Mathf.Max(movementSpeed += (Input.GetAxis("Mouse ScrollWheel") * 0.5f), 0.01f);
        transform.position += (transform.right * Input.GetAxis("Horizontal") + transform.forward * Input.GetAxis("Vertical") + transform.up * Input.GetAxis("Depth")) * movementSpeed;
        if (Input.GetButton("Fire2")) {
            transform.eulerAngles += new Vector3(-Input.GetAxis("Mouse Y"), Input.GetAxis("Mouse X"), Input.GetAxis("Rotation"));
        } else {
            transform.eulerAngles += new Vector3(0.0f, 0.0f, Input.GetAxis("Rotation"));
        }
    }
}
