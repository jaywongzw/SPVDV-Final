//
//  SearchViewController.swift
//  CognitoYourUserPoolsSample
//
//  Created by JZ on 11/15/17.
//  Copyright © 2017 Dubal, Rohan. All rights reserved.
//

import UIKit

class SearchViewController: UIViewController {
    
    let client = SEARCHDevawsnodejsClient.default 

    @IBOutlet var Plate: UITextField!
    @IBOutlet var Location: UITextField!
    @IBOutlet var Result: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

//    @IBAction func add(_ sender: Any) {
//        let first = Int(Plate.text!)
//        let second = Int(Location.text!)
//        let output =  Int(first! + second!)
//        Result.text = "This Result: \(output) "
//    }
//    
//    @IBAction func Minus(_ sender: Any) {
//        let first = Int(Plate.text!)
//        let second = Int(Location.text!)
//        let output =  Int(first! - second!)
//        Result.text = "This Result: \(output) "
//    }
    
    @IBAction func Pop(_ sender: Any) {
        let popOverVC = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "popupID") as! PopUpViewController
        popOverVC.plate = self.Plate.text
        self.addChildViewController(popOverVC)
        popOverVC.view.frame = self.view.frame
        self.view.addSubview(popOverVC.view)
        popOverVC.didMove(toParentViewController: self)
    }
    
    @IBAction func Pop2(_ sender: Any) {
        let popOverVC = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "popupID2") as! PopUp2ViewController
        popOverVC.location = self.Location.text
        self.addChildViewController(popOverVC)
        popOverVC.view.frame = self.view.frame
        self.view.addSubview(popOverVC.view)
        popOverVC.didMove(toParentViewController: self)
    }
    
}
