import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Question } from './models/question.model';

@Injectable({
  providedIn: 'root'
})
export class TestService {
  questions:Question[]=[] 
  url = 'http://127.0.0.1:3000/api/calls/questions';
  constructor(private http: HttpClient) { }


  getQuestions(){
   
  
    // Define the required query parameters
    const params = new HttpParams()
      .set('email', 'david@email.com') 
      .set('limit', '10') 
      .set('difficulty', '1'); 
  
    // Make the HTTP GET request with the specified parameters
   return this.http.get<any>(this.url, { params })

  }
  postQuestions(){
    const params = new HttpParams()
      .set('email', 'david@email.com') 
      .set('question', '18')
      .set('correct', 'True')
    
    return this.http.post(this.url,{params})
  /*  *Request.body:*
| Parameter   | Type     | Description                                         |
| :--------   | :------- | :---------------------------------------------------|
| `email`     | `string` | **Required**. Email address of a user.              |
| `question`  | `string` | **Required**. Question user answered.               |
| `correct`   | `boolean`| **Required**. True/False if user answered correctly.
*/

}

}
