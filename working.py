from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional #better autocomplete for deelper, not necessary but best practice
#To create Item class, use Pydantic's BaseN=Model:
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    brand:Optional[str]=None #optional parameter


class UpdateItem(BaseModel):
    name:Optional[str] = None
    price:Optional[float] = None
    brand:Optional[str]=None 



inventory = {}

#example of path parameter
@app.get('/get-item/{item_id}')
def get_item(item_id:int=Path(description="The ID of the item you'd like to view")):
    raise HTTPException(status_code=404, detail="Item ID not found") #can also use: status_code=status.HTTP_404_NOT_FOUND



#example query parameter
@app.get('/get-by-name') #parameter not in endpoint = query parameter automatically
def get_item(name:Optional[str]=None): #adding "None" makes it an optional parameter, so if I don't have a name I don't get an error, I just get no data
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        raise HTTPException(status_code=404, detail="Item name not found") #can also use: status_code=status.HTTP_404_NOT_FOUND



#combine both:
@app.get("/get-by-name-number/{item_id}")
def get_using_both(test:int,item_id:int, name:Optional[str]=None):
    for item_id in inventory:
        if inventory[item_id]['name'] == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item number not found") #can also use: status_code=status.HTTP_404_NOT_FOUND



#Create an item in inventory: Pass Item in  request body
@app.post('/create-item/{item_id}')
def create_item(item_id:int, item:Item):
    if item_id in inventory:
            raise HTTPException(status_code=400, detail="Item already exists") 
    inventory[item_id]=item       #no need to do this, just insert the objec and fastAPI will automatically jasonify{"name":item.name, "brand":item.brand, "price":item.price}   
    return inventory[item_id]



@app.put('/update-item/{item_id}')
def update_item(item_id:int, item: UpdateItem):
    if item_id not in inventory:
            raise HTTPException(status_code=404, detail="Item ID does not exist") 

    
    if item.name != None:
        inventory[item_id].name = item.name
        inventory[item_id].price = item.price
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete('/delete-item')
def delete_item(item_id:int = Query(...,description="ID of the item you wish to delete")):
    if item_id not in inventory:
        return {"Error":"ID does not exist"}
    del inventory[item_id]
    return{"Success":"Item deleted!"}


#to run this: uvicorn working:app --reload