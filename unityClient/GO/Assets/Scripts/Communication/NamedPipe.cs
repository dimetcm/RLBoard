using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.IO.Pipes;


public class NamedPipe : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if ( Input.GetKeyDown( KeyCode.A ) )
        {
            using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "DMXServer", PipeDirection.InOut))
            {

                // Connect to the pipe or wait until the pipe is available.
                Debug.Log("Attempting to connect to pipe...");
                pipeClient.Connect();

                Debug.Log("Connected to pipe.");
                int numberOfServerInstances = pipeClient.NumberOfServerInstances;
                // Debug.LogFormat("There are currently {0} pipe server instances open.", pipeClient.NumberOfServerInstances.ToString());
                using (StreamReader sr = new StreamReader(pipeClient))
                {
                    // Display the read text to the console
                    string temp;
                    while ((temp = sr.ReadLine()) != null)
                    {
                        Debug.LogFormat("Received from server: {0}", temp);
                    }
                }
            }
            Debug.Log("Press Enter to continue...");
            //Console.ReadLine();
        }
    }
}
