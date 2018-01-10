//
//  PopUp2ViewController.swift
//  CognitoYourUserPoolsSample
//
//  Created by JZ on 11/16/17.
//  Copyright © 2017 Dubal, Rohan. All rights reserved.
//

import UIKit
import Foundation
import AWSCore

class PopUp2ViewController: UIViewController {
    
    let client = SEARCHDevawsnodejsClient.default()
    //?locat=SJSU%20South
    @IBOutlet weak var apiMsg: UILabel!
    
    var location: String? = nil
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = UIColor.black.withAlphaComponent(0.8)
        client.spaceGet(Locat: "locat", Name: location!).continueWith{ ( task: AWSTask? ) -> AnyObject? in
            if let error = task?.error {
                print("Error occurred: \(error)")
                return nil
            }
            
            if let result = task?.result {
                if  result.count == 0 {
                    DispatchQueue.main.async {
                        self.apiMsg.text = "Cannot find anything"
                    }
                }
                 print("Result is : \(result)")
                 DispatchQueue.main.async {
                    self.apiMsg.text = "Result is : \(result)"
                }
            }
            return nil
        }
        
        self.showAnimate()
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func ClosePop(_ sender: Any) {
        self.removeAnimate()
    }
    
    
    func showAnimate()
    {
        self.view.transform = CGAffineTransform(scaleX: 1.3, y: 1.3)
        self.view.alpha = 0.0;
        UIView.animate(withDuration: 0.25, animations: {
            self.view.alpha = 1.0
            self.view.transform = CGAffineTransform(scaleX: 1.0, y: 1.0)
        });
    }
    
    func removeAnimate()
    {
        UIView.animate(withDuration: 0.25, animations: {
            self.view.transform = CGAffineTransform(scaleX: 1.3, y: 1.3)
            self.view.alpha = 0.0;
        }, completion:{(finished : Bool)  in
            if (finished)
            {
                self.view.removeFromSuperview()
            }
        });
    }
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    
}

