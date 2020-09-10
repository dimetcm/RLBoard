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

    private List<GoStone> m_whiteStones = new List<GoStone>();
    private List<GoStone> m_blackStones = new List<GoStone>();

    public enum StoneColor
    {
        White,
        Black
    }

    private StoneColor m_currentPlayerColor = StoneColor.White;
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
        GoStone stone = new GoStone(intersection.X, intersection.Y);
        if  (!m_whiteStones.Contains(stone) && !m_blackStones.Contains(stone))
        {
            if (m_currentPlayerColor == StoneColor.White)
            {
                m_whiteStones.Add(stone);
            }
            else
            {
                m_blackStones.Add(stone);
            }
            m_boardVisual.PlaceStone(intersection, m_currentPlayerColor);
            m_currentPlayerColor = m_currentPlayerColor == StoneColor.White ? StoneColor.Black : StoneColor.White;
        }

    }
}
