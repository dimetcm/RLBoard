using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;

public class GoGame : MonoBehaviour
{
    [SerializeField]
    private int m_size = 9;


    [SerializeField]
    private GoBoardVisual m_boardVisual = null;

    private static GoGame m_instance = null;

    public enum PlayerColor
    {
        White,
        Black
    }

    private PlayerColor m_currentPlayerColor = PlayerColor.White;
    public static GoGame Instance
    {
        get 
        {
            Assert.IsNotNull(m_instance);
            return m_instance;
        }
    }

    public int Size
    {
        get { return m_size; }
    }

    void Awake()
    {
        Assert.IsNull(m_instance);
        m_instance = this;
    }

    // Start is called before the first frame update
    void Start()
    {
        m_boardVisual.Init(m_size);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void OnClicked(GoBoardIntersection intersection)
    {
        m_boardVisual.PlaceStone(intersection, m_currentPlayerColor);
        m_currentPlayerColor = m_currentPlayerColor == PlayerColor.White ? PlayerColor.Black : PlayerColor.White;
    }
}
