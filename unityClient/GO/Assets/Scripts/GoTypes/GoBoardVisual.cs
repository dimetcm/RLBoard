using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoBoardVisual : MonoBehaviour
{
    [SerializeField]
    float m_boardSize = 0.9f;

    [SerializeField]
    GameObject m_linePrefab = null;
    [SerializeField]
    GameObject m_linesContainer = null;

    [SerializeField]
    GameObject m_intersectionPrefab = null;
    [SerializeField]
    GameObject m_intersectionsContainer = null;

        for (int i = 0; i < m_boardLogic.Size + 1; ++i)
    GameObject m_whitePlayerStonePrefab = null;
    [SerializeField]
    GameObject m_blackPlayerStonePrefab = null;
    [SerializeField]
    GameObject m_stonesContainer = null;

    // Start is called before the first frame update

    public void Init(int boardSize)
    {
        for (int i = 0; i < boardSize + 1; ++i)
        {
            float boardLength = 10.0f;
            float boardOffset = m_boardSize * boardLength * 0.5f;
            float step = (m_boardSize * boardLength) / boardSize;

            {
                var line = Instantiate(m_linePrefab, m_linesContainer.transform, false);
                line.transform.localScale = new Vector3(boardLength * m_boardSize, 0.03f, 1.0f);
                line.transform.localPosition = new Vector3(0.0f, 0.0f, i * step - boardOffset);
            }

            {
                var line = Instantiate(m_linePrefab, m_linesContainer.transform, false);
                line.transform.localScale = new Vector3(0.03f, boardLength * m_boardSize, 1.0f);
                line.transform.localPosition = new Vector3(i * step - boardOffset, 0.0f, 0.0f);
            }

            for (int j = 0; j < boardSize + 1; ++j)
            {
                var intersection = Instantiate(m_intersectionPrefab, m_intersectionsContainer.transform, false);
                intersection.transform.localPosition = new Vector3(i * step - boardOffset, 0.0f, j * step - boardOffset);
            }
        }

    }

    public void PlaceStone(GoBoardIntersection intersection, GoGame.PlayerColor playerColor)
    {
        GameObject stonePrefab = playerColor == GoGame.PlayerColor.White ? m_whitePlayerStonePrefab : m_blackPlayerStonePrefab;
        Instantiate(stonePrefab, intersection.transform.position, intersection.transform.rotation, m_stonesContainer.transform);

    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
