import React from 'react';
import { Link } from 'react-router-dom';


const Book2 = ({itemData}) => {
  console.log(itemData)
  return (
    <div className='book-item flex flex-column flex-sb'>
      <div className='book-item-img'>
        <img src = {itemData.img_url} alt = "cover" />
      </div>
      <div className='book-item-info text-center'>
        
          
            <span>{itemData.title}</span>
         
       

        
       
      </div>
    </div>
  )
}

export default Book2