using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoBoardIntersection : MonoBehaviour
{
    void OnMouseDown()
    {
        GoGame.Instance.OnClicked(this);
    }
}
