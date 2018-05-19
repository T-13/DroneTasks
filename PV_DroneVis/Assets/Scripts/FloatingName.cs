using UnityEngine;

public class FloatingName : MonoBehaviour {

    public float textSize = 30;

	// Update is called once per frame
	void Update() {
        // Orient name towards the Main Camera (actually aways as it is inverted) and scale it with distance
        Vector3 textScreenSpace = Camera.main.WorldToScreenPoint(transform.position);
        Vector3 adjustedScreenSpace = new Vector3(textScreenSpace.x + textSize, textScreenSpace.y, textScreenSpace.z);
        Vector3 adjustedWorldSpace = Camera.main.ScreenToWorldPoint(adjustedScreenSpace);
        transform.localScale = Vector3.one * (transform.position - adjustedWorldSpace).magnitude;
        transform.rotation = Camera.main.transform.rotation;
    }
}
