using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoardVisual : MonoBehaviour
{
    Board m_boardLogic = null;
    [SerializeField]
    float m_boardSize = 0.9f;
    [SerializeField]
    GameObject m_lineRendererPrefab = null;
    [SerializeField]
    GameObject m_linesContainer = null;
    void Awake()
    {
        m_boardLogic = GetComponent<Board>();

        //GameObject.Get
        //gameObject linesContainer = Get
        for (int i = 0; i < m_boardLogic.Size + 1; ++i)
        {
            float step = (m_boardSize * 10.0f) / m_boardLogic.Size;

            {
                var line = Instantiate(m_lineRendererPrefab, m_linesContainer.transform, false);
                line.transform.localScale = new Vector3(10.0f * m_boardSize, 0.03f, 1.0f);
                line.transform.localPosition = new Vector3(0.0f, 0.0f, i * step - m_boardSize * 5.0f);
            }

            {
                var line = Instantiate(m_lineRendererPrefab, m_linesContainer.transform, false);
                line.transform.localScale = new Vector3(0.03f, 10.0f * m_boardSize, 1.0f);
                line.transform.localPosition = new Vector3(i * step - m_boardSize * 5.0f, 0.0f, 0.0f);
            }

            //float lineLength = m_boardSize * 0.5f;
            //float step = m_boardSize / m_boardLogic.Size;


            //line.SetPosition(0, new Vector3(-lineLength + step * i, 0.0f, -lineLength));
            //line.SetPosition(1, new Vector3(-lineLength + step * i, 0.0f, lineLength));
            //line.transform.SetParent(m_linesContainer.transform);
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
