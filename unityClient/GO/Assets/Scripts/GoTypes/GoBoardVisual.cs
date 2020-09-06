using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoBoardVisual : MonoBehaviour
{
    GoBoard m_boardLogic = null;
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
    void Awake()
    {
        m_boardLogic = GetComponent<GoBoard>();

        for (int i = 0; i < m_boardLogic.Size + 1; ++i)
        {
            float boardLength = 10.0f;
            float boardOffset = m_boardSize * boardLength * 0.5f;
            float step = (m_boardSize * boardLength) / m_boardLogic.Size;

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

            for (int j = 0; j < m_boardLogic.Size + 1; ++j)
            { 
                var intersection = Instantiate(m_intersectionPrefab, m_intersectionsContainer.transform, false);
                intersection.transform.localPosition = new Vector3(i * step - boardOffset, 0.0f, j * step - boardOffset);
            }
        }
        
    }
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
