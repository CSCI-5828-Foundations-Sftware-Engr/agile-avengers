## Get summary by category

URI: /v1/summary/<user-id>/category

### Response

- Status code: 200
  Response: 
  ```json
   {
  "Apparel": 540.0,
  "Beauty": 295.0,
  "Food": 115.0,
  "Insurance": 860.0,
  "Sports": 220.0
   }
  ```

- Status code: 404
  Response: 
  ```json
  {
    "message": "user not found"
  }
  ```

## Get summary by sub_category

URI: /v1/summary/<user-id>/subcategory

### Response

- Status code: 200
  Response: 
  ```json
   {
  "Accessories": 295.0,
  "Car": 860.0,
  "Eating out": 115.0,
  "Equipment": 220.0,
  "Laundry": 540.0
  }
  ```

- Status code: 404
  Response: 
  ```json
  {
    "message": "user not found"
  }
  ```

## Get summary by merchant

URI: /v1/summary/<user-id>/merchant

### Response

- Status code: 200
  Response: 
  ```json
   {
  "Baker, Nichols and Manning": 220.0,
  "Bowman, Padilla and Curry": 115.0,
  "Leon and Sons": 540.0,
  "Short and Sons": 860.0,
  "Young-Rivera": 295.0
  }
  ```

- Status code: 404
  Response: 
  ```json
  {
    "message": "user not found"
  }
  ```