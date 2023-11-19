import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http:HttpClient) { }


  checkUsername(email: string) {
    const url = 'http://127.0.0.1:3000/api/users/exists';
    const params = new HttpParams().set('email', email);
    return this.http.get(url, {params});
  
  }
  createUser(userInfo:any){
    return this.http.post('http://127.0.0.1:3000/api/users/create', userInfo);
    }
 
    authUser(loginInfo:any){
      return this.http.post('http://127.0.0.1:3000/api/users/auth',loginInfo)
    }
  }



