using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.IO.Pipes;

public class CommunicationManager
{
    NamedPipeClientStream m_pipeClient;

    public void Connect()
    {
        using (m_pipeClient = new NamedPipeClientStream(".", "GOPipe", PipeDirection.InOut))
        {

            // Connect to the pipe or wait until the pipe is available.
            Debug.Log("Attempting to connect to pipe...");
            m_pipeClient.Connect();
        }
    }
}
