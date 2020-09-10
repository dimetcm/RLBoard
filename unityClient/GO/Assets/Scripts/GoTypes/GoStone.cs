using System.Collections;
using System;
using System.Collections.Generic;
public class GoStone : IEquatable<GoStone>
{
    private int m_x;
    private int m_y;

    public GoStone(int x, int y)
    {
        m_x = x;
        m_y = y;
    }

    public bool Equals(GoStone other)
    {
        return m_x == other.m_x && m_y == other.m_y;
    }
}
