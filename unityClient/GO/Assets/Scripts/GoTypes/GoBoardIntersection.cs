using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoBoardIntersection : MonoBehaviour
{
    public int m_x;
    public int m_y;

    public void Init(int x, int y)
    {
        m_x = x;
        m_y = y;
    }

    public int X { get { return m_x; } }
    public int Y { get { return m_y; } }
    void OnMouseDown()
    {
        GoGame.Instance.OnClicked(this);
    }
}
