import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Question } from './models/question.model';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TestService {
  questions:Question[]=[] 
  url = 'https://learnmath-backend-532124fc8334.herokuapp.com/api/calls/questions';
  constructor(private http: HttpClient) { }


  getQuestions(user, difficulty){
    // Define the required query parameters
    console.log("getQuestions user", user)
    const params = new HttpParams()
      .set('email', user) 
      .set('limit', '10') 
      .set('difficulty', difficulty); 
  
    // Make the HTTP GET request with the specified parameters
   return this.http.get<any>(this.url, { params })

  }

  postQuestions(data) {
   console.log("data", data)
    const postQuestion = (index = 0) => {
      if (index < data.length) {
        console.log('data index', data[index])
        this.http.post(this.url, data[index]).subscribe(
          response => {
            console.log('Successfully sent to the server:', response);
            postQuestion(index + 1); // Call the next item in the array
          },
          error => {
            console.error('Error sending to the server:', error);
            postQuestion(index + 1); // Continue with the next item even if there is an error
          }
        );
      } else {
        console.log('All items have been processed');
        
      }
    };
    
   postQuestion()
}

}
