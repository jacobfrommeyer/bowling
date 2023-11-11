using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class randomNum : MonoBehaviour
{
    // private int testNum = 5;
    private string num = "0";
    public Text test;

    // public void onButtonPress(){
    //     if(Input.GetKeyDown(KeyCode.Space)){
    //         num = (Random.Range(0, 10)).ToString();
    //         Update(num);
    //     }
    //     // return num;
    // }

    void Update(){
        if(Input.GetKeyDown(KeyCode.Space)){
            num = (Random.Range(0, 10)).ToString();
        }

        test.text = "Random number: " + num;
    }

    public void onClick(){
        num = (Random.Range(0, 10)).ToString();
        test.text = "Random number: " + num;
    }
}
