from urllib.request import Request, urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import json
from flask import Flask, json


    
class MyClass:
    """Interface"""
        
    def printJson(self, data):
        print(json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
        ))
        
    def getAll(self,data,cat):
        retDic = []
        drinkList = []
        for thing in data['Data']['categoriesList']:
            if thing['categoryName'] == cat:
                drinkList = thing['dishList']
                break
            
        for drink in drinkList:
            retDic.append(
                 { 'dishId':drink['dishId'],
                    'dishName':drink['dishName'],
                   "dishDescription":drink["dishDescription"],
                   "dishPrice":drink["dishPrice"]
                   }  
                )
        return retDic
    
    def getOne(self,data,cat, idNum):
        m =self.getAll(data,cat)
        print("mmmmmmmmmmm",m)
        for item in m:
            if idNum == item["dishId"]:
                return item
                
                
      
        


def dealWithIO(data,path):
    
    inter = MyClass()
##    inter.printJson(data)
    li=path.split("/")
    li= li[1:]
    cat=li[0]
    
    if cat =="drinks":cat = "Drinks"
    if cat =="pizzas ":cat = "Pizzas"
    if cat =="desserts ":cat = "Desserts"
    if cat =="drink":cat = "Drink"
    if cat =="pizza":cat = "Pizza"
    if cat =="dessert":cat = "Dessert"
    
    # if plural,
    if len(li) == 1:
        tu=inter.getAll(data, cat)
        return tu
    else:
        ans =inter.getOne(data,cat,li[1])
        return ans
        
        
        





def main():
    req = Request('https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup',
              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})
    webpage = urlopen(req, timeout=10).read()
    data = json.loads(webpage)
    api = Flask(__name__)

    @api.route('/drinks', methods=['GET'])
    def get_drinks():
        return json.dumps(dealWithIO(data,"/drinks"))
    
    @api.route('/drink/id', methods=['GET'])
    def get_desserts():
        return json.dumps(dealWithIO(data,"/drink/2055846"))
    

    if __name__ == '__main__':
        api.run(debug=True)

    
    
    
##    dealWithIO(data,"/drinks")
    dealWithIO(data,"/drink/id")
##    dealWithIO(data,"/pizza/id")
##    dealWithIO(data,"/pizzas")
    


if __name__ == "__main__":
    main()
